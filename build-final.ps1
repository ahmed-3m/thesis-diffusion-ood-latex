#requires -Version 5.1
<#
.SYNOPSIS
    Build the final submission PDF for the JKU MSc thesis.

.DESCRIPTION
    Runs the XeLaTeX + Biber + XeLaTeX + XeLaTeX sequence required for the
    jkureport template to settle all cross-references, the bibliography,
    the table of contents, the list of figures, and the list of tables.
    On success, copies the resulting main-thesis.pdf to the official
    submission filename in the same directory.

.NOTES
    Submission filename pattern:
        <Term>-<MatrNr>-<LastName>_<FirstName>-Thesis_MSc-<Version>-<Topic>.pdf
        26SS-K12035954-Mohammed_Ahmed-Thesis_MSc-v3-Diffusion_OOD_Detection.pdf

    Prerequisites:
        - TeX Live or MiKTeX with XeLaTeX and Biber on PATH
        - All .tex sources and references.bib in the current directory

.EXAMPLE
    .\build-final.ps1
        Run from D:\side_hustle\thesis\draft02\submission-v2\
#>

[CmdletBinding()]
param(
    [string]$MainStem        = 'main-thesis',
    [string]$SubmissionName  = '26SS-K12035954-Mohammed_Ahmed-Thesis_MSc-v3-Diffusion_OOD_Detection.pdf',
    [switch]$KeepAux
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

function Assert-Tool($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Required tool '$name' was not found on PATH. Install TeX Live or MiKTeX and ensure '$name' is reachable."
    }
}

Assert-Tool xelatex
Assert-Tool biber

Write-Host "==> Pass 1/4: xelatex (initial)"           -ForegroundColor Cyan
& xelatex -interaction=nonstopmode -halt-on-error "$MainStem.tex" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "xelatex pass 1 failed (exit $LASTEXITCODE). See $MainStem.log." }

Write-Host "==> Pass 2/4: biber (bibliography)"        -ForegroundColor Cyan
& biber $MainStem | Out-Null
if ($LASTEXITCODE -ne 0) { throw "biber failed (exit $LASTEXITCODE). See $MainStem.blg." }

Write-Host "==> Pass 3/4: xelatex (resolve refs)"      -ForegroundColor Cyan
& xelatex -interaction=nonstopmode -halt-on-error "$MainStem.tex" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "xelatex pass 3 failed (exit $LASTEXITCODE). See $MainStem.log." }

Write-Host "==> Pass 4/4: xelatex (settle TOC/LOF/LOT)" -ForegroundColor Cyan
& xelatex -interaction=nonstopmode -halt-on-error "$MainStem.tex" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "xelatex pass 4 failed (exit $LASTEXITCODE). See $MainStem.log." }

$pdfIn  = Join-Path $here "$MainStem.pdf"
$pdfOut = Join-Path $here $SubmissionName

if (-not (Test-Path -LiteralPath $pdfIn)) {
    throw "Expected output '$pdfIn' was not produced."
}

Copy-Item -LiteralPath $pdfIn -Destination $pdfOut -Force
Write-Host ""
Write-Host "==> Build OK" -ForegroundColor Green
Write-Host "    Source PDF      : $pdfIn"
Write-Host "    Submission PDF  : $pdfOut"

# Surface citation/reference warnings without blocking the build, since
# the LaTeX engine already exits non-zero on hard errors above.
$log = Get-Content -LiteralPath (Join-Path $here "$MainStem.log") -Raw
$undef = ([regex]::Matches($log, 'LaTeX Warning: (Citation|Reference) [^\r\n]+ undefined')).Count
if ($undef -gt 0) {
    Write-Warning "$undef undefined citation/reference warnings in $MainStem.log -- review before final submission."
} else {
    Write-Host "    Cross-references: all resolved (0 undefined warnings)" -ForegroundColor Green
}

if (-not $KeepAux) {
    Write-Host ""
    Write-Host "==> Aux files retained (pass -KeepAux:`$false to remove). Tip: 'git clean -X' removes them when committed via .gitignore."
}
