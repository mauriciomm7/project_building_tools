import argparse
import os
import shutil
from pathlib import Path

# Define templates
templates = {
    "1": {"name": "Basic Jupyter Notebook", "path": "basic.ipynb"},
    "2": {"name": "Data Science Template", "path": "data_science.ipynb"},
    "3": {"name": "Machine Learning Template", "path": "machine_learning.ipynb"},
}

def display_menu():
    print("[bold]Available Templates:[/bold]")
    for key, value in templates.items():
        print(f"{key}. {value['name']}")

def copy_template(template_path, output_name, output_dir=None):
    # CREATE output_dir variable with name
    if output_dir is None:
        output_path = Path(output_name).with_suffix(".ipynb")
    else:
        output_path = (Path(output_dir) / output_name).with_suffix(".ipynb")
    
    try:
    # CREATE copy of template using output_path with error handling
        shutil.copy(template_path, output_path)
        print(f"Template copied to {output_path}")
    except FileNotFoundError:
        print(f"Template file {template_path} not found.")

def main():
    parser = argparse.ArgumentParser(description='Create a new Jupyter Notebook from a template.')
    parser.add_argument('name', type=str, help='Name of the new notebook')
    parser.add_argument('-l', '--location', type=str, help='Optional location path for the new notebook', default=None)
    args = parser.parse_args()

    display_menu()
    choice = input("Enter the number of your chosen template: ")

    if choice in templates:
        template_path = templates[choice]["path"]
        
        if args.location:
            output_dir = Path(args.location)
            if not output_dir.exists():
                print(f"Location {output_dir} does not exist. Creating directory...")
                output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = None
        
        copy_template(template_path, args.name, output_dir)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
