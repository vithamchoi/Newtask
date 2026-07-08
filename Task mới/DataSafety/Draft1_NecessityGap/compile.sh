#!/usr/bin/env bash
# Build the Necessity Gap manuscript.
# Requires a TeX Live distribution with elsarticle, tikz, pgfplots.
set -e
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode main.tex
bibtex   main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
echo "Build complete: $(pwd)/main.pdf"
