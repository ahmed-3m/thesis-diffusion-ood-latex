# Conditional Diffusion Models for OOD Detection

This repository contains the LaTeX source, figures, bibliography, and build assets for the Master's thesis:

**Conditional Diffusion Models for Out-of-Distribution Detection and Industrial Quality Control**

## Abstract

Out-of-distribution (OOD) detection is a critical challenge for safe machine learning. This thesis treats conditional diffusion models as generative classifiers: class-conditional reconstruction error serves as the OOD signal.

The work develops a binary conditional diffusion model (CDM) for CIFAR-10 OOD detection on an airplane-vs-rest split and introduces a class-conditional separation loss that widens the gap between class-conditional noise predictions. With no separation loss, the binary CDM reaches `92.52% +/- 11.07%` AUROC across three seeds; with `lambda = 0.02`, performance rises to `99.03% +/- 0.07%`.

The thesis also tests transfer to industrial inkjet quality classification using the public `InkjetOOD` pipeline and the public FTI_Zer0P dataset. The inkjet experiments show an important boundary condition: separation loss improves CIFAR-10 OOD detection strongly, but does not automatically transfer to small, fine-grained industrial datasets.

![Cross-domain separation-loss comparison](images/fig_cross_domain_comparison.png)

## Public Artefacts

- CIFAR-10/OOD code: [DiffusionOOD](https://github.com/ahmed-3m/DiffusionOOD)
- Inkjet quality-control code: [InkjetOOD](https://github.com/ahmed-3m/InkjetOOD)
- Public inkjet dataset: [FTI_Zer0P on Zenodo](https://doi.org/10.5281/zenodo.11444566)

## Build

Use XeLaTeX and Biber:

```powershell
xelatex main-thesis.tex
biber main-thesis
xelatex main-thesis.tex
xelatex main-thesis.tex
```

The generated `main-thesis.pdf` and auxiliary LaTeX build files are intentionally ignored by Git.
