from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import zipfile
import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from .scanner import scan_project, generate_tree
from .language_detector import detect_language
from .parsers import parse_python_file, parse_js_file
from .extractors.dependency_extractor import extract_dependencies
from .extractors.api_extractor import extract_api_routes
from .extractors.graph_extractor import build_dependency_graph
from .documentation.markdown_generator import generate_markdown, save_docs
from .comparison.readme_comparator import compare_readme
from .utils.converter import md_to_pdf

app = FastAPI(title="AI Code-to-Doc Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="code_to_doc/static"), name="static")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "generated_docs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return FileResponse("code_to_doc/static/index.html")


def process_single_file(f_path, project_path):
    """
    Helper function for parallel processing.
    """
    lang = detect_language(f_path)
    rel_path = os.path.relpath(f_path, project_path)
    
    if lang == "python":
        file_meta = parse_python_file(f_path)
        file_meta["path"] = rel_path
        file_meta["language"] = lang
        routes = extract_api_routes(f_path, lang)
        deps = extract_dependencies(f_path, lang)
        return {"type": "python", "meta": file_meta, "routes": routes, "deps": deps}
    elif lang in ["javascript", "typescript"]:
        file_meta = parse_js_file(f_path)
        file_meta["path"] = rel_path
        file_meta["language"] = lang
        return {"type": "js", "meta": file_meta, "deps": file_meta.get("imports", [])}
    return None

@app.post("/analyze")
async def analyze_project(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are supported")
    
    session_id = str(uuid.uuid4())
    project_path = os.path.join(UPLOAD_DIR, session_id)
    zip_path = os.path.join(UPLOAD_DIR, f"{session_id}.zip")
    
    # Save and extract ZIP
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to extract ZIP: {str(e)}"})

    # Process project
    all_files = scan_project(project_path)
    project_tree = generate_tree(project_path)
    
    extracted_metadata = {
        "project_tree": project_tree,
        "files": [],
        "api_routes": [],
        "all_dependencies": set(),
        "technologies": set()
    }
    
    # Process files in parallel
    with ProcessPoolExecutor() as executor:
        func = partial(process_single_file, project_path=project_path)
        results = list(executor.map(func, all_files))
        
    for res in results:
        if not res: continue
        
        extracted_metadata["files"].append(res["meta"])
        extracted_metadata["technologies"].add(res["meta"].get("language", "Unknown"))
        if "routes" in res:
            extracted_metadata["api_routes"].extend(res["routes"])
        if "deps" in res:
            extracted_metadata["all_dependencies"].update(res["deps"])
            
    extracted_metadata["all_dependencies"] = list(extracted_metadata["all_dependencies"])
    extracted_metadata["technologies"] = list(extracted_metadata["technologies"])
    
    # Build dependency graph (Advanced)
    graph = build_dependency_graph(extracted_metadata)
    extracted_metadata["dependency_graph"] = graph
    
    # Comparison
    comparison = compare_readme(project_path, extracted_metadata)
    extracted_metadata["readme_comparison"] = comparison
    
    # Generate Markdown
    md_content = generate_markdown(extracted_metadata)
    doc_path = os.path.join(OUTPUT_DIR, f"{session_id}_docs.md")
    save_docs(md_content, doc_path)
    
    # Cleanup (optional but recommended)
    # shutil.rmtree(project_path)
    # os.remove(zip_path)
    
    return {
        "session_id": session_id,
        "metadata": extracted_metadata,
        "markdown_url": f"/docs/{session_id}",
        "comparison": comparison
    }

@app.get("/download/{session_id}")
async def download_pdf(session_id: str):
    md_path = os.path.join(OUTPUT_DIR, f"{session_id}_docs.md")
    pdf_path = os.path.join(OUTPUT_DIR, f"{session_id}_docs.pdf")
    
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Documentation not found")
        
    # Convert to PDF if not already exists
    if not os.path.exists(pdf_path):
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        success = md_to_pdf(md_content, pdf_path)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
            
    return FileResponse(pdf_path, filename=f"project_documentation_{session_id}.pdf", media_type="application/pdf")

@app.get("/docs/{session_id}")
async def get_markdown(session_id: str):
    md_path = os.path.join(OUTPUT_DIR, f"{session_id}_docs.md")
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Documentation not found")
    return FileResponse(md_path, media_type="text/markdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
