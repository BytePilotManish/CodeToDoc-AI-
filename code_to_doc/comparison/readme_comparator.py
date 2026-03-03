import os

def find_readme(root_path):
    """
    Finds a README file in the root or one level deep.
    """
    possible_names = ["README.md", "README.markdown", "readme.md", "README"]
    
    # Check root
    for name in possible_names:
        path = os.path.join(root_path, name)
        if os.path.exists(path):
            return path
            
    # Check one level deep (in case of folder-in-zip)
    try:
        items = os.listdir(root_path)
        if len(items) == 1 and os.path.isdir(os.path.join(root_path, items[0])):
            for name in possible_names:
                path = os.path.join(root_path, items[0], name)
                if os.path.exists(path):
                    return path
    except:
        pass
        
    return None

def compare_readme(root_path, extracted_metadata):
    """
    Compares existing README with extracted metadata to find missing documentation.
    """
    readme_path = find_readme(root_path)
    if not readme_path:
        return {"status": "No README found"}
    
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
    except Exception as e:
        return {"status": f"Error reading README: {str(e)}"}
    
    missing_classes = []
    missing_functions = []
    
    for file_info in extracted_metadata.get("files", []):
        for cls in file_info.get("classes", []):
            if cls["name"].lower() not in content:
                missing_classes.append(cls["name"])
        
        for func in file_info.get("functions", []):
            if func["name"].lower() not in content:
                missing_functions.append(func["name"])
                
    return {
        "missing_classes": missing_classes,
        "missing_functions": missing_functions,
        "summary": f"Found {len(missing_classes)} missing classes and {len(missing_functions)} missing functions in README"
    }

