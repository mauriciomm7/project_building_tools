"""
CLI Utility — Project Folder Scaffolder

Usage:
    python create_project_structure.py <target_location> <project_name> [tex_base_path]

Description:
    Creates a standardized directory structure for a new project. Includes boilerplate files
    like README.md and .gitignore, and generates a `paths.py` module with easy-to-use
    constants pointing to all key folders.

Arguments:
    <target_location>   Where to create the new project directory.
    <project_name>      Name of the new project folder.
    [tex_base_path]     Optional. Path to the academic paper's LaTeX project directory
                       (i.e., the source files of the paper accompanying this code).
                       If provided, LaTeX-specific paths (figures, tables, bibliography)
                       will be added as constants in the generated `paths.py`.

Result:
    - Creates folders like: data/, scripts/, utils/, notebooks/, figures/
    - Adds starter files (README.md, .gitignore, __init__.py)
    - Outputs a `paths.py` for import in other modules, including LaTeX paths if specified.

Example (Windows):
    >>> python create_project_structure.py C:\\Users\\yourname\\projects my_project C:\\Users\\yourname\\paper_latex_project
"""

import os
import sys

def prompt_confirm_dirname(directory_name):
    RED = "\033[91m"
    RESET = "\033[0m"
    prompt = f"Directory {RED}'{directory_name}'{RESET} already exists. To confirm {RED}overwrite{RESET}, please type the project name exactly: "
    while True:
        response = input(prompt).strip()
        if response == directory_name:
            return True
        else:
            print(f"Input did not match '{directory_name}'. Please try again.")
            print("Exiting...")
            break

def create_project_structure(
    target_location,
    project_name,
    directories,
    file_map=None,
    tex_base=None
):
    """
    Create a project directory structure with optional boilerplate files and paths.py generation.

    Args:
        target_location (str): Location to create the project directory.
        project_name (str): Name of the main project directory.
        directories (list): List of subdirectories to create within the project.
        file_map (dict): Mapping from subdirectory path (relative to root) to list of files.
        tex_base (str): Optional. Base path to a LaTeX project for generating LaTeX-related constants.

    Returns:
        None
    """
    # Static boilerplate file contents
    file_contents = {
        ".gitignore": (
            "# Ignore Python compiled files\n"
            "*.pyc\n"
            "__pycache__/\n"
            "_quarto.yml\n"
            ".env\n"
            "raw/*.csv\n"
            "raw/*.zip\n\n"
            "# IGNORE ALL RStudio Crap\n"
            "*.Rproj\n"
            ".RData\n"
            ".Rhistory\n"
            ".Ruserdata\n"

        ),  
        "README.md": (
            "# Project Title\n\n"
            "A brief description of your project.\n\n"
            "## Project Structure Usage\n\n"
            "- The `data` directory holds cleaned and structured datasets used for analysis.\n"
            "- The `figures` directory is for publication-ready figures.\n"
            "- The `nbs` directory is for Jupyter or Quarto notebooks.\n"
            "- The `raw` directory contains the raw input datasets (scraped or external).\n"
            "- The `scripts` directory is for stand-alone scripts supporting the project.\n"
            "- The `utils` directory is for module-like utilities for the project.\n"
        ),
        
        ".vscode/settings.json": (
            '{\n'
            '  "files.exclude": {\n'
            '    "**/*.Rproj": true,\n'
            '    "**/.RData": true,\n'
            '    "**/.Rhistory": true,\n'
            '    "**/.Ruserdata": true,\n'
            '    "**/Rplot*.png": true\n'
            '  }\n'
            '}'
        ),
        "scripts/__init__.py": "",
        "utils/__init__.py": "",
        
    }

    # Prevent overrite
    project_path = os.path.join(target_location, project_name)
    
    if os.path.exists(project_path):
        if not prompt_confirm_dirname(project_name):
            print("Operation aborted by user.")
            sys.exit(0)
        else:
            print(f"Confirmed overwrite of '{project_name}'. Proceeding...")
        
    # Create main project directory
    os.makedirs(project_path, exist_ok=True)

    # Create subdirectories
    for directory in directories:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)

    # Create files in specified locations
    if file_map:
        for subdir, files in file_map.items():
            for file in files:
                rel_path = os.path.join(subdir, file) if subdir else file
                abs_path = os.path.join(project_path, rel_path)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                normalized_rel_path = rel_path.replace(os.sep, "/")  # normalize path separators
                if normalized_rel_path in file_contents:
                    # print(f"Writing file: {rel_path}, normalized: {normalized_rel_path}, found content: {normalized_rel_path in file_contents}")
                    with open(abs_path, 'w') as f:
                        f.write(file_contents[normalized_rel_path])


    # Generate paths.py inside utils/
    utils_dir = os.path.join(project_path, 'utils')
    os.makedirs(utils_dir, exist_ok=True)
    paths_file_path = os.path.join(utils_dir, 'paths.py')
    
    with open(paths_file_path, 'w') as paths_file:
        paths_file.write("# Automatically generated file for accessing project folders.\n\n")
        paths_file.write("import os\n\n")
        paths_file.write("REPO_DIR = os.path.abspath(os.path.dirname(__file__))\n\n")

        for directory in directories:
            if directory == ".vscode":
                # Skip creating .vscode folder here
                continue
            const_name = f"{directory.upper()}_DIR"
            paths_file.write(f"{const_name} = os.path.join(REPO_DIR, '{directory}')\n")

        if tex_base:
            paths_file.write("\n#####################################\n")
            paths_file.write(f"TEX_BASE = r'{tex_base}'\n")
            paths_file.write("TEX_BIB_FILE = os.path.join(TEX_BASE, 'references.bib')\n")
            paths_file.write("TEX_FIG_DIR = os.path.join(TEX_BASE, 'figures')\n")
            paths_file.write("TEX_TAB_DIR = os.path.join(TEX_BASE, 'tables')\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: python create_project_structure.py <target_location> <project_name> [tex_base_path]")
        sys.exit(1)

    target_location = sys.argv[1]
    project_name = sys.argv[2]
    tex_base = sys.argv[3] if len(sys.argv) > 3 else None

    # Define your standard directories
    directories = ["data", "results", "raw", "figures", "scripts", "nbs", "utils", ".vscode"]

    # Define file locations ("" = root directory)
    file_map = {
        "": ["README.md", "requirements.txt", ".gitignore",],
        "scripts": ["__init__.py"],
        "utils": ["__init__.py"],
        ".vscode": ["settings.json"]

    }

    create_project_structure(target_location, project_name, directories, file_map, tex_base)
    print(f"Project structure created successfully in {os.path.join(target_location, project_name)}.")

if __name__ == "__main__":
    main()
