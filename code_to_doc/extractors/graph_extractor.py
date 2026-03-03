import networkx as nx
import os

def build_dependency_graph(extracted_metadata):
    """
    Builds a dependency graph and returns a Mermaid-compatible string.
    """
    G = nx.DiGraph()
    
    # Add nodes for each file
    for file_info in extracted_metadata.get("files", []):
        rel_path = file_info["path"]
        G.add_node(rel_path)
        
        # Add edges based on imports/dependencies
        for dep in file_info.get("imports", []):
            dep_parts = dep.split('.')
            
            for other_file in extracted_metadata.get("files", []):
                other_path = other_file["path"].replace("\\", "/")
                # Get the module path (e.g., backend/models.py -> backend.models)
                other_module = os.path.splitext(other_path)[0].replace("/", ".")
                
                # Check if the import matches the module or the filename
                other_name = os.path.splitext(os.path.basename(other_path))[0]
                
                if rel_path != other_file["path"] and (
                    other_module.endswith(dep) or 
                    dep.startswith(other_module) or
                    any(part == other_name for part in dep_parts)
                ):
                    G.add_edge(rel_path, other_file["path"])

                    
    return generate_mermaid_graph(G)

def generate_mermaid_graph(G):
    """
    Converts a NetworkX graph to Mermaid graph syntax.
    """
    if not G.nodes:
        return ""
        
    mermaid = "graph TD\n"
    for edge in G.edges():
        u, v = edge
        mermaid += f"    {sanitize_name(u)} --> {sanitize_name(v)}\n"
        
    # Also add single nodes
    for node in G.nodes():
        if G.degree(node) == 0:
            mermaid += f"    {sanitize_name(node)}\n"
            
    return mermaid

def sanitize_name(name):
    """
    Sanitizes file paths for Mermaid compatibility.
    """
    return name.replace("/", "_").replace("\\", "_").replace(".", "_").replace("-", "_")
