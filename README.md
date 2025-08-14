# Project Building Tools

Handy scripts for automating the creation of project directories, README files, and other essential structures. Boost your productivity with these project-building tools.

## TODO

- [ ] REVIEW how to convert *.ipynb to .md files to be deployed in main website: https://github.com/matteocourthoud/Data-Science-Python/blob/main/convert.sh
- [ ] CREATE `.ipynb`, `.R`, `.py`, `.qmd` YAML files for every project.

### PDF Converters (ilovepdf akin)

### `_format_converters`

- [ ] Convert into terminal app that gets initialized on on a dir, reads .md files, lets you choose format.
- [ ] ADD _format_converters\ md to html for website deployment.
- [ ] UPDATE the project constructor so that creates links for latex presentations too.
- [ ] CREATE a template for very narrow but satble tasks, such as paper/student feedback sparringly.
- [ ] UPDATE paper_converter.py
- [ ] CONSIDER handling of codeblocs

## Log History


Date:  søndag 3. august 2025 11:03:07200

- [X] ADDED `.gitatributes` to project constructor.
- [X] ADDED `_pyprojects\*` new subproject for making notebook templates.

Date:   Sat Aug 2 18:26:02 2025 +0200

- [X] ADDED `.vscode/settings.json` to project constructor.

Date:   Tue Apr 22 22:14:10 2025 -0400

- [ ] ADDED `cbatchinstall` for installing packages across envs

Date:

- [X] ADDED base path cosntrcutor for latex files

```python
#tex_base = {here goes your base path for latex}
tex_bib_file = os.path.join(tex_base, bibliography.bib)
tex_fig_dir = os.path.join(tex_base, "figures")
tex_tab_dir = os.path.join(tex_base, "tables") 
```

- [X] CREATE SHELL script that exports Conda ENVs YML everytime they are modified.
- [X] CREATE md to pdf format converter _format_converters

Date: Fri May 31 16:18:55 2024 +0200

- Added new custom functions script for WindowsPowerShell.ps1

Date: Tue June 24

- Added TODO file, and addedd experimental paper_convert@0.2.py
