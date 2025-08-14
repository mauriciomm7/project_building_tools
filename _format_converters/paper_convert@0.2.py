##################################################################
# PANDOC MARKDOWN TO PDF CONVERTER WITH CUSTOM STYLING
# 
# Usage: python script.py <sourcefile> <outputfile> [--bib file.bib] [--logo logo.png]
##################################################################

import argparse
import subprocess
import os
from pathlib import Path

# CONSTANTS - Single source of truth for all help information
FORMATTING_RULES = {
    'horizontal_rule': {
        'wrong': '---',
        'correct': '***',
        'reason': 'creates YAML parsing errors'
    },
    'negative_numbers': {
        'wrong': '−3.83',  # Unicode minus U+2212
        'correct': '-3.83',  # Regular hyphen U+002D
        'reason': 'causes LaTeX Unicode errors'
    }
}

TROUBLESHOOTING_TIPS = [
    f"Replace '{FORMATTING_RULES['horizontal_rule']['wrong']}' with '{FORMATTING_RULES['horizontal_rule']['correct']}' for horizontal rules",
    f"Replace '{FORMATTING_RULES['negative_numbers']['wrong']}' with '{FORMATTING_RULES['negative_numbers']['correct']}' in negative numbers",
    "Complete all incomplete markdown sections",
    "Check that all file paths are correct"
]

def validate_file_exists(filepath, file_type):
    """Single function to validate file existence."""
    if filepath is not None and not os.path.isfile(filepath):
        raise FileNotFoundError(f"{file_type} file '{filepath}' not found.")

def build_pandoc_command(input_file, output_file, bib, logo):
    """Build the pandoc command with all necessary parameters."""
    command = [
        "pandoc", input_file, "-o", output_file,
        "--pdf-engine=xelatex",  # Handles Unicode properly
        "--variable", "author:Mauricio Mandujano M.",
        "--variable", "documentclass:article",
        "--variable", "fontsize:12pt",
        "--variable", "geometry:margin=.75in",
        "--variable", "fontfamily:Libertinus",
        "--variable", "mainfont:Times New Roman",
        "--variable", "sansfont:Arial", 
        "--variable", "monofont:JetBrains Mono",
        "--variable", "colorlinks:true",
        "--variable", "linkcolor:blue",
        "--variable", "urlcolor:cyan",
        "--variable", "toc:true",
        "--highlight-style=pygments",
    ]
    
    if bib is not None:
        command.extend(["--bibliography", bib, "--variable", "biblio-style:chicago"])
    
    if logo is not None:
        command.extend(["--variable", f"logo:{logo}"])
    
    return command

def print_troubleshooting_help():
    """Print standardized troubleshooting information."""
    print("Common fixes:")
    for tip in TROUBLESHOOTING_TIPS:
        print(f"   - {tip}")

def convert_to_pdf(input_file, output_file, bib=None, logo=None):
    """
    Convert Markdown to PDF using Pandoc with academic styling.
    
    Important: Use '***' not '---' for horizontal rules, and '-' not '−' for negative numbers.
    """
    
    # VALIDATE all files exist
    validate_file_exists(input_file, "Input")
    validate_file_exists(bib, "Bibliography")
    validate_file_exists(logo, "Logo")
    
    # BUILD and execute pandoc command
    pandoc_command = build_pandoc_command(input_file, output_file, bib, logo)
    
    try:
        subprocess.run(pandoc_command, check=True)
        
        print("PDF conversion successful!")
        print(f"File location: {os.path.abspath(output_file)}")
        print(f"Directory: {Path(output_file).parent}")
        
        # Auto-open PDF (Windows)
        subprocess.run(f'start "" "{output_file}"', check=True, shell=True)
        
    except subprocess.CalledProcessError:
        print("Pandoc conversion failed!")
        print_troubleshooting_help()
        raise

def main():
    """Main function with command-line argument parsing."""
    
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PDF with academic styling",
        epilog=f"""
Formatting Rules:
• Horizontal rules: Use '{FORMATTING_RULES['horizontal_rule']['correct']}' not '{FORMATTING_RULES['horizontal_rule']['wrong']}'
• Negative numbers: Use '{FORMATTING_RULES['negative_numbers']['correct']}' not '{FORMATTING_RULES['negative_numbers']['wrong']}'
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("output_file", help="Path to output PDF file")
    parser.add_argument("--bib", help="Path to bibliography file (.bib)", default=None)
    parser.add_argument("--logo", help="Path to logo image file", default=None)
    
    args = parser.parse_args()
    
    try:
        convert_to_pdf(args.input_file, args.output_file, args.bib, args.logo)
    except FileNotFoundError as e:
        print(f"File Error: {e}")
    except Exception as e:
        print(f"Conversion Error: {e}")
        print_troubleshooting_help()

if __name__ == "__main__":
    main()
