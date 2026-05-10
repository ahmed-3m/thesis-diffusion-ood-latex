# Thesis LaTeX Source

This repository contains the LaTeX source and assets needed to compile:

`main-thesis.tex`

## Build

Use XeLaTeX and Biber:

```powershell
xelatex main-thesis.tex
biber main-thesis
xelatex main-thesis.tex
xelatex main-thesis.tex
```

The generated `main-thesis.pdf` is intentionally ignored by Git.
