import os
import re
import numpy as np


# FUNCTION Definitions

def is_valid_folder_name(input_str):
    # Use regular expression to check for special characters
    # ^ and $ ensure the entire string is matched
    # \w matches any word character (letters, digits, or underscore)
    # \s matches any whitespace character
    # If the input contains only word characters and spaces, it's considered valid
    return bool(re.match(r'^[\w\s]+$', input_str))

def normalize_folder_name(input_str):
    # Convert to lowercase and replace spaces with underscores
    return input_str.lower().replace(" ", "_")

def get_valid_folder_name():
    while True:
        user_input = input("Enter a folder name (letters, digits, or spaces only): ")
        if is_valid_folder_name(user_input):
            return user_input
        else:
            print("Invalid input. Folder name can only contain letters, digits, or spaces.")

def get_valid_directory(prompt="Enter a valid directory path: "):
    while True:
        user_input = input(prompt)
        if os.path.exists(user_input) and os.path.isdir(user_input):
            return user_input
        else:
            print("Invalid input. Please enter a valid directory path.")

def create_project_structure(directory_path, normalized_name):
    # Create the base directory
    base_directory = os.path.join(directory_path, normalized_name)
    os.makedirs(base_directory, exist_ok=True)

    # Create README.md
    with open(os.path.join(base_directory, 'README.md'), 'w') as readme_file:
        readme_file.write("# " + normalized_name + "\n\n")

    # Create subdirectories
    subdirectories = ['_code', '_data', '_src', '_slides', '_manuscript']
    for subdir in subdirectories:
        os.makedirs(os.path.join(base_directory, subdir), exist_ok=True)

    # Create subdirectories within _slides and _manuscript
    sub_subdirectories = ['_images']
    for subdir in sub_subdirectories:
        os.makedirs(os.path.join(base_directory, '_slides', subdir), exist_ok=True)
        os.makedirs(os.path.join(base_directory, '_manuscript', subdir), exist_ok=True)


# CREATE MAIN FUNCTION 
print("""
Welcome, this is a project builder. It will create the following folders with their respective subfolders:
_Code
_Data
_Experiment
_SCR
_Slides
""")

project_name = get_valid_folder_name()
normalized_name = normalize_folder_name(project_name)
print("Folder name:", normalized_name)
print("*******************************************************")
directory_path = get_valid_directory()
print("You entered a valid directory path:", directory_path)

create_project_structure(directory_path, normalized_name)
print("Project structure created successfully.")