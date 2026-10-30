import os
from langchain_core.tools import tool

PROJECT_ROOT = "generated_project"

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file inside the generated project directory."""
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    full_path = os.path.join(PROJECT_ROOT, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"

@tool
def read_file(path: str) -> str:
    """Reads content from a file inside the generated project directory."""
    full_path = os.path.join(PROJECT_ROOT, path)
    if not os.path.exists(full_path):
        return "File does not exist yet."
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def list_files() -> list:
    """Lists all files generated in the project directory."""
    if not os.path.exists(PROJECT_ROOT):
        return []
    return os.listdir(PROJECT_ROOT)

coder_tools = [write_file, read_file, list_files]
