import argparse
import subprocess
import os

def convert_to_pdf(input_file, output_file, bib=None, logo=None, no_toc=False):
    """
    Convert a Markdown file to PDF using Pandoc with custom styling options.

    Parameters:
    - input_file (str): Path to the input Markdown file.
    - output_file (str): Path to the output PDF file.
    - bib (str, optional): Path to bibliography file (.bib). Default is None.
    - logo (str, optional): Path to logo image (.png). Default is None.
    - no_toc (bool, optional): If True, do not include table of contents. Default is False.
    """
    
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    if bib is not None and not os.path.isfile(bib):
        raise FileNotFoundError(f"Bibliography file '{bib}' not found.")
    if logo is not None and not os.path.isfile(logo):
        raise FileNotFoundError(f"Logo file '{logo}' not found.")
    
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
        "--highlight-style=pygments",
    ]
    
    if not no_toc:
        pandoc_command.extend(["--variable", "toc:true"])
    if bib is not None:
        pandoc_command.extend(["--bibliography", bib, "--variable", "biblio-style:chicago"])
    if logo is not None:
        pandoc_command.extend(["--variable", f"logo:{logo}"])
    
    subprocess.run(pandoc_command, check=True)
    print(f"\n✅ File created at:\n{os.path.abspath(output_file)}\n")

    # Open output (on Windows)
    start_command = ["start", output_file]
    subprocess.run(start_command, check=True, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF with custom Pandoc settings.")
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("output_file", help="Path to the output file (e.g., .pdf, .html).")
    parser.add_argument("--bib", help="Path to bibliography file (.bib), optional.", default=None)
    parser.add_argument("--logo", help="Path to logo file (.png), optional.", default=None)
    parser.add_argument("--no-toc", action="store_true", help="Exclude table of contents.")

    args = parser.parse_args()

    try:
        convert_to_pdf(args.input_file, args.output_file, args.bib, args.logo, args.no_toc)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
