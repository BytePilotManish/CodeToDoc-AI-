import os

def generate_markdown(metadata):
    """
    Generates structured Markdown from extracted code metadata.
    """
    md = f"# Project Documentation\n\n"
    
    if metadata.get("project_tree"):
        md += f"## Folder Structure\n```\n{metadata['project_tree']}\n```\n\n"
    
    if metadata.get("overview"):
        md += f"## 1. Project Overview\n{metadata['overview']}\n\n"
    else:
        md += f"## 1. Project Overview\n"
        md += f"> [!TIP]\n> **Technologies Used**: {', '.join(metadata.get('technologies', ['Unknown']))}\n\n"
        md += f"### Architecture Summary\n"
        md += f"The project follows a modular structure focused on {', '.join(metadata.get('technologies', []))} development. "
        md += f"It consists of {len(metadata.get('files', []))} core source files.\n\n"
    
    if metadata.get("project_tree"):
        md += f"## 2. Folder Structure Explanation\n"
        md += f"```\n{metadata['project_tree']}\n```\n"
        md += f"> [!NOTE]\n> **Directory Purposes**:\n"
        # We can hardcode some common ones or infer from names
        if "backend" in metadata['project_tree'].lower():
            md += f"> - `backend/`: Contains server-side logic and API endpoints.\n"
        if "frontend" in metadata['project_tree'].lower():
            md += f"> - `frontend/`: Contains client-side components and UI logic.\n"
        if "parsers" in metadata['project_tree'].lower():
            md += f"> - `parsers/`: Specialized logic for code analysis.\n"
        md += "\n"

    if metadata.get("dependency_graph"):
        md += f"## 3. High-Level Architecture (Visual)\n\n```mermaid\n{metadata['dependency_graph']}\n```\n\n"
    
    # Modules / Files
    md += f"## 4. Module-Level Documentation\n\n"
    for file_info in metadata.get("files", []):
        md += f"### File: `{file_info['path']}`\n"
        if file_info.get("docstring"):
            md += f"{file_info['docstring']}\n\n"
        else:
            md += f"> [!NOTE]\n> **Inferred**: This module contains source code but lacks a top-level docstring.\n\n"
        
        # React Components (special case for JS)
        if file_info.get("components"):
            md += "#### React Components\n"
            for comp in file_info["components"]:
                md += f"- **Component: `{comp['name']}`**\n"
                md += f"  - *Type*: {comp['type']}\n"
                if comp.get("props"):
                    md += f"  - *Props*: `{', '.join(comp['props'])}`\n"
                else:
                    md += f"  - *Props*: None detected\n"
                
                # State Management (Hooks)
                if file_info.get("hooks"):
                    md += f"  - *State/Hooks*: `{', '.join(file_info['hooks'])}`\n"
                
                # Routing (if any in this file)
                if file_info.get("routes"):
                    md += f"  - *Detected Routes*: `{', '.join(file_info['routes'])}`\n"
            md += "\n"


        # Classes
        if file_info.get("classes"):
            md += "#### Classes\n"
            for cls in file_info["classes"]:
                md += f"- **Class: `{cls['name']}`**\n"
                if cls.get("docstring"):
                    md += f"  - *Description*: {cls['docstring']}\n"
                else:
                    md += f"  - > [!NOTE]\n  - > **Inferred**: No class-level docstring found.\n"
                if cls.get("methods"):
                    md += "  - *Methods*:\n"
                    for method in cls["methods"]:
                        md += f"    - `{method['name']}({', '.join(method['parameters'])})`\n"
            md += "\n"
        
        # Functions
        if file_info.get("functions"):
            md += "#### Functions\n"
            for func in file_info["functions"]:
                md += f"- **`{func['name']}({', '.join(func['parameters'])})`**\n"
                if func.get("docstring") and func["docstring"] != "No docstring found":
                    md += f"  - *Description*: {func['docstring']}\n"
                else:
                    md += f"  - > [!NOTE]\n  - > **Inferred**: No function docstring found.\n"
            md += "\n"
            
    # API Documentation
    if metadata.get("api_routes"):
        md += "## 5. API Documentation\n\n"
        md += "| Method | Endpoint / Function | Request Params | Description |\n"
        md += "| --- | --- | --- | --- |\n"
        for route in metadata["api_routes"]:
            params = route.get("parameters", "N/A")
            md += f"| {route['method']} | {route['function']} | `{params}` | {route.get('docstring', 'No description')} |\n"
        
        md += "\n> [!IMPORTANT]\n> **Response Structure**: Typically returns JSON. Specific schemas are inferred from return statements.\n"
    
    # README Comparison (Scenario 3)
    if metadata.get("readme_comparison"):
        comparison = metadata["readme_comparison"]
        md += "## 6. Documentation Gap Analysis (README.md)\n\n"
        
        if comparison.get("status") == "No README.md found":
            md += "> [!WARNING]\n> **No existing README.md found** in the project root. It is highly recommended to create one using the content above as a base.\n\n"
        else:
            md += f"### {comparison.get('summary', 'Summary')}\n\n"
            
            if comparison.get("missing_classes"):
                md += "#### Missing Classes in README\n"
                md += "The following classes are present in the code but not mentioned in your README.md:\n"
                for cls in comparison["missing_classes"]:
                    md += f"- `{cls}`\n"
                md += "\n"
                
            if comparison.get("missing_functions"):
                md += "#### Missing Functions in README\n"
                md += "The following functions are present in the code but not mentioned in your README.md:\n"
                for func in comparison["missing_functions"]:
                    md += f"- `{func}`\n"
                md += "\n"
                
            md += "> [!TIP]\n> **Suggested Updates**: Consider adding sections for these missing components to your README.md to ensure parity between your code and its high-level documentation.\n\n"
            
    return md


def save_docs(md_content, output_path="docs/documentation.md"):
    """
    Saves the generated Markdown to a file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    return output_path
