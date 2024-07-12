import os
import sys

def create_project_structure(target_location, project_name, directories, files, file_contents=None):
    """
    Create project directory structure.

    Args:
        target_location (str): The target location where the project directory will be created.
        project_name (str): The name of the project directory.
        directories (list): List of subdirectories to be created within the project directory.
        files (list): List of files to be created within the project directory.
        file_contents (dict): Optional. A dictionary where keys are filenames and values are the text to be added to those files.

    Returns:
        None
    """
    # Create the main project directory
    project_path = os.path.join(target_location, project_name)
    os.makedirs(project_path, exist_ok=True)
    
    # Create subdirectories
    for directory in directories:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)
    
    # Create files
    for file in files:
        file_path = os.path.join(project_path, file)
        with open(file_path, 'a') as f:
            if file_contents and file in file_contents:
                f.write(file_contents[file])
    
    # Generate paths.py file
    with open(os.path.join(project_path, 'paths.py'), 'w') as paths_file:
        paths_file.write(f"# Automatically generated file for accessing correct folders. \n\n")
        paths_file.write(f"import os\n\n")
        paths_file.write(f"rep_dir = os.path.abspath(os.path.dirname(__file__))\n\n")
        for directory in directories:
            paths_file.write(f"{directory}_dir = os.path.join(rep_dir, '{directory}')\n")
        paths_file.write(f"#####################################\n\n " )
        paths_file.write(f"# Add your Latex paths here")
        
if __name__ == "__main__":
    # Ensure proper usage
    if len(sys.argv) < 3:
        print("Usage: python create_project_structure.py <target_location> <project_name>")
        sys.exit(1)
    
    # Extract target location and project name from command line arguments
    target_location = sys.argv[1]
    project_name = sys.argv[2]
    
    # Define the directories and files for the project structure
    directories = ["data", "results", "raw", "figures"]
    files = ["README.md", "requirements.txt", ".gitignore"]
    
    # Define contents for specific files
    file_contents = {
        ".gitignore": "# Ignore Python compiled files\n*.pyc\n__pycache__/\n._qarto.yml",
        "README.md": "# Project Title\n\nA brief description of your project."
    }
    
    # Call the function to create the project structure
    create_project_structure(target_location, project_name, directories, files, file_contents)
    print(f"Project structure created successfully in {os.path.join(target_location, project_name)}.")

