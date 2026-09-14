@echo off
chcp 65001 > nul
echo ========================================================
echo   Compilando Todos os Documentos - Pratica 5
echo ========================================================
cd /d "%~dp0"

echo.
echo [1/2] Compilando Proposta (proposta_main.tex)...
pdflatex -interaction=nonstopmode proposta_main.tex > nul
bibtex proposta_main > nul
pdflatex -interaction=nonstopmode proposta_main.tex > nul
pdflatex -interaction=nonstopmode proposta_main.tex > nul

echo [2/2] Compilando Relatorio (modelo_praticas_main.tex)...
pdflatex -interaction=nonstopmode modelo_praticas_main.tex > nul
bibtex modelo_praticas_main > nul
pdflatex -interaction=nonstopmode modelo_praticas_main.tex > nul
pdflatex -interaction=nonstopmode modelo_praticas_main.tex > nul

echo.
echo ========================================================
echo   [CONCLUIDO] Documentos gerados com sucesso:
echo   - proposta_main.pdf
echo   - modelo_praticas_main.pdf
echo ========================================================
pause
