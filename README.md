# AI Code-to-Doc Generator

An AI-powered automated documentation generator that transforms codebases into structured technical documentation (Markdown & PDF).

## 🏗️ Architecture Diagram

The following diagram illustrates the data flow and modular structure of the system:

```mermaid
graph TD
    A[User Upload / ZIP] --> B[FastAPI Backend (main.py)]
    B --> C[Project Scanner]
    C --> D[Language Detector]
    D --> E{File Type?}
    E -->|Python| F[Python AST Parser]
    E -->|JS/React| G[JS Pattern Parser]
    F --> H[Metadata Extractor]
    G --> H
    H --> I[Dependency & Graph Extractor]
    I --> J[Markdown Generator]
    J --> K[PDF Converter]
    K --> L[Output: MD & PDF Docs]
```

## 🛠️ Setup Instructions

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd assisto-task1
   ```

2. Install the required dependencies:

   ```bash
   pip install -r code_to_doc/requirements.txt
   ```

### Running the Application

1. Start the FastAPI server:

   ```bash
   python -m code_to_doc.main
   ```

2. Open your browser and navigate to:
   `http://localhost:8000`
3. Upload a ZIP file of your code repository and click **Generate Documentation**.

## 🎨 Design Decisions

1. **Static Analysis Only**: For security and speed, the system uses Python's `ast` module and regex patterns for JavaScript. It **never executes** the user's code, preventing malicious script execution during analysis.
2. **Inferred Documentation**: When source code lacks docstrings, the system uses "Inference Logic" to provide context (e.g., "Inferred: No docstring found") instead of leaving blank sections.
3. **Multiprocessing**: To handle projects larger than 10,000 lines of code (LOC) within the 3-minute performance requirement, file analysis is parallelized using `ProcessPoolExecutor`.
4. **Glassmorphism UI**: The web interface uses modern CSS aesthetics (vibrant colors, blur effects) to provide a premium user experience compared to standard documentation tools.

## 📝 Assumptions

1. **Project Format**: The system assumes projects are uploaded as `.zip` files.
2. **Supported Languages**: Currently optimized for Python (`.py`) and JavaScript/TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`). Other file types are listed in the folder structure but not deeply analyzed.
3. **API Patterns**: Route extraction is optimized for popular frameworks like FastAPI, Flask, and Express (pattern matching).
4. **Dependencies**: Accurate dependency graphing depends on standard import statements (e.g., `import x`, `from x import y`, `import x from 'y'`).
