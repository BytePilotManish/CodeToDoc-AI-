import os

def scan_project(root_path, exclude_dirs=None):
    """
    Scans a project directory and returns a list of all file paths.
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build'}
    
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def generate_tree(root_path, exclude_dirs=None):
    """
    Generates a string representation of the project folder structure.
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build'}
        
    tree = ""
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(root_path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree += f"{subindent}{f}\n"
    return tree
