#!/bin/bash
echo "[1/2] Compilando Proposta..."
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode proposta_main.tex > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive bibtex proposta_main > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode proposta_main.tex > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode proposta_main.tex > /dev/null

echo "[2/2] Compilando Relatorio..."
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode modelo_praticas_main.tex > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive bibtex modelo_praticas_main > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode modelo_praticas_main.tex > /dev/null
docker run --rm -v "$PWD":/workdir -w /workdir texlive/texlive pdflatex -interaction=nonstopmode modelo_praticas_main.tex > /dev/null

echo "Concluído!"
