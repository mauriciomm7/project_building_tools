# Project Building Tools

Handy scripts for automating the creation of project directories, README files, and other essential structures. Boost your productivity with these project-building tools.

## TODO

- [ ] UPDATE the project constructor so that creates links for latex presentations too.
- [ ] REVIEW how to convert *.ipynb to .md files to be deployed in main website: https://github.com/matteocourthoud/Data-Science-Python/blob/main/convert.sh
- [ ] ADD _format_converters\ md to html for website deployment.
- [ ] CREATE `.ipynb`, `.R`, `.py`, `.qmd` YAML files for every project.
- [ ] ADD base path cosntrcutor for latex files

```python
#tex_base = {here goes your base path for latex}
tex_bib_file = os.path.join(tex_base, bibliography.bib)
tex_fig_dir = os.path.join(tex_base, "figures")
tex_tab_dir = os.path.join(tex_base, "tables") 
```

- [X] CREATE SHELL script that exports Conda ENVs YML everytime they are modified.
- [X] CREATE md to pdf format converter _format_converters

## Log History

Date:   Fri May 31 16:18:55 2024 +0200

- Added new custom functions script for WindowsPowerShell.ps1
