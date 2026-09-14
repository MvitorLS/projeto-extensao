@echo off
chcp 65001 > nul
echo ========================================================
echo   Compilando Proposta (proposta_main.tex) - Pratica 3
echo ========================================================
cd /d "%~dp0"

echo [1/4] Primeira passagem pdflatex...
pdflatex -interaction=nonstopmode proposta_main.tex > nul

echo [2/4] Processando bibliografia bibtex...
bibtex proposta_main > nul

echo [3/4] Segunda passagem pdflatex (ajuste de referencias)...
pdflatex -interaction=nonstopmode proposta_main.tex > nul

echo [4/4] Terceira passagem pdflatex (ajuste de sumario/paginas)...
pdflatex -interaction=nonstopmode proposta_main.tex

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   [SUCESSO] proposta_main.pdf gerado com sucesso!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [AVISO] Verifique proposta_main.log se houver alertas.
    echo ========================================================
)
pause
