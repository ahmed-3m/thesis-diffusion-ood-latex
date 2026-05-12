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

## Writing Checks

Install the project-local writing tools:

```powershell
npm install
```

Run the free local checks:

```powershell
npm run lint:writing
npm run lint:ai-style
```

Expose the project-local textlint setup as an MCP server, for editors or
agents that support MCP:

```powershell
npm run mcp:textlint
```

Run the optional grammar check through the free public LanguageTool API:

```powershell
npm run lint:languagetool -- 00-abstract.tex
```

The AI-style check is a conservative phrase scanner, not a scientific AI detector.

Vale rules are also included in `.vale/` for anyone who already has the
Vale CLI available, but Vale is not installed as a project dependency because
the npm wrapper currently pulls vulnerable transitive packages.
