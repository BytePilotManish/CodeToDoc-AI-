import os

def detect_language(file_path):
    """
    Detects the programming language based on the file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".cpp": "cpp",
        ".h": "cpp",
        ".c": "c"
    }
    
    return mapping.get(ext)
