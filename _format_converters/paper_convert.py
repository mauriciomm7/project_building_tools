##################################################################
# CREATE parameters <sourcefile> <outputfile> <bib> <logo>
# "example.md" "example.pdf" OR "example.html" OR "example.docx"
##################################################################
import argparse
import subprocess
import os


# FUNCTION to run the Pandoc command with custom variables
def convert_to_pdf(input_file, output_file, bib=None, logo=None):
    """
    Parameters:
    - input_file (str): Path to the input Markdown file.
    - output_file (str): Path to the output PDF file.
    - bib (str, optional): Path to the bibliography file (.bib). If None, no bibliography is added. Default is None.
    - logo (str, optional): Path to the logo file (.png). If None, no logo is added. Default is None.

    Example Usage:
     - To convert `input.md` to `output.pdf` with only a logo:
      python convert_to_pdf.py "input.md" "output.pdf" --logo "path/to/logo.png"
    """
    
    # CHECK if input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    
    # CHECK if bibliography file exists if provided
    if bib is not None and not os.path.isfile(bib):
        raise FileNotFoundError(f"Bibliography file '{bib}' not found.")
    
    # CHECK if logo file exists if provided
    if logo is not None and not os.path.isfile(logo):
        raise FileNotFoundError(f"Logo file '{logo}' not found.")
    
    # CUSTOM Pandoc command with all variables
    pandoc_command = [
        "pandoc", input_file,
        "-o", output_file,
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
    
    # ONLY add the bibliography if it's provided (not None)
    if bib is not None:
        pandoc_command.extend(["--bibliography", bib, "--variable", "biblio-style:chicago"])
    
    # ONLY add the logo if it's provided (not None)
    if logo is not None:
        pandoc_command.extend(["--variable", f"logo:{logo}"])
    
    # RUN the Pandoc command using subprocess
    subprocess.run(pandoc_command, check=True)
    # DONE provide feedback 
    print(f"You can find you file here:\n\n{os.path.abspath(output_file)}\n")
    
    # [ ] ADD START subprocess 
    start_command = ["start", output_file]
    subprocess.run(start_command, check=True, shell=True)

# MAIN function to handle argument parsing
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF with custom Pandoc settings.")
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("output_file", help="Path to the output PDF file.")
    parser.add_argument("--bib", help="Path to the bibliography file (.bib), set to None to omit", default=None)
    parser.add_argument("--logo", help="Path to the logo file (.png), set to None to omit", default=None)
    
    args = parser.parse_args()
    
    # CALL the function to convert the file
    try:
        convert_to_pdf(args.input_file, args.output_file, args.bib, args.logo)
    except FileNotFoundError as e:
        print(f"Error: {e}")
