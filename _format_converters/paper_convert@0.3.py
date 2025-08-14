##################################################################
# CREATE parameters <sourcefile> <outputfile> <bib> <logo> <image-dir>
# "example.md" "example.pdf"
##################################################################
import argparse
import subprocess
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def convert_to_pdf(input_file, output_file, bib=None, logo=None, image_dir=None):
    """
    Convert a Markdown file to PDF using Pandoc with custom settings.

    Parameters:
    - input_file (str): Path to the input Markdown file.
    - output_file (str): Path to the output PDF file.
    - bib (str, optional): Path to the bibliography file (.bib).
      If None, no bibliography is added.
    - logo (str, optional): Path to the logo file (.png).
      If None, no logo is added.
    - image_dir (str, optional): Path to directory containing images.

    Example:
      python convert_to_pdf.py "input.md" "output.pdf" --logo "path/to/logo.png"
    """

    # Check input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    # Check bibliography file exists if provided
    if bib is not None and not os.path.isfile(bib):
        raise FileNotFoundError(f"Bibliography file '{bib}' not found.")

    # Check logo file exists if provided
    if logo is not None and not os.path.isfile(logo):
        raise FileNotFoundError(f"Logo file '{logo}' not found.")

    # Default image scaling for PDF
    latex_image_scale = r"""
    \usepackage{graphicx}
    \usepackage{float}
    \let\oldincludegraphics\includegraphics
    \renewcommand{\includegraphics}[2][]{\oldincludegraphics[width=0.7\linewidth]{#2}}
    \let\origfigure\figure
    \let\endorigfigure\endfigure
    \renewenvironment{figure}[1][]{\origfigure[H]}{\endorigfigure}
    """


    with NamedTemporaryFile(delete=False, suffix=".tex") as tmp_header:
        tmp_header.write(latex_image_scale.encode("utf-8"))
        tmp_header_path = tmp_header.name

    # Pandoc base command
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
        "--include-in-header", tmp_header_path
    ]

    # Add bibliography if provided
    if bib is not None:
        pandoc_command.extend([
            "--bibliography", bib,
            "--variable", "biblio-style:chicago"
        ])

    # Add logo if provided
    if logo is not None:
        pandoc_command.extend(["--variable", f"logo:{logo}"])

    # Add image directory support if provided
    if image_dir is not None:
        pandoc_command.extend(["--resource-path", image_dir])

    try:
        # Run Pandoc
        subprocess.run(pandoc_command, check=True)

        # Feedback
        print(f"This is your filepath:\n\n{os.path.abspath(output_file)}\n")
        print(f"You can find your file here:\n{Path(output_file).parent}\n")

        # Open the file automatically
        start_command = f'start "" "{output_file}"'
        subprocess.run(start_command, check=True, shell=True)

    finally:
        # Cleanup temp LaTeX header file
        if os.path.exists(tmp_header_path):
            os.remove(tmp_header_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PDF with custom Pandoc settings."
    )
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("output_file", help="Path to the output PDF file.")
    parser.add_argument(
        "--bib",
        help="Path to the bibliography file (.bib), set to None to omit",
        default=None
    )
    parser.add_argument(
        "--logo",
        help="Path to the logo file (.png), set to None to omit",
        default=None
    )
    parser.add_argument(
        "--image-dir",
        help="Path to directory containing images",
        default=None
    )

    args = parser.parse_args()

    try:
        convert_to_pdf(
            args.input_file,
            args.output_file,
            args.bib,
            args.logo,
            args.image_dir
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
