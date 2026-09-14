@echo off
chcp 65001 > nul
echo ========================================================
echo   Compilando Tudo: Pratica 3 e Pratica 5...
echo ========================================================

echo.
echo === COMPILANDO PRATICA 3 ===
cd /d "%~dp0\Pratica 3"
call compilar_tudo.bat

echo.
echo === COMPILANDO PRATICA 5 ===
cd /d "%~dp0\Pratica 5"
call compilar_tudo.bat

echo.
echo ========================================================
echo   [CONCLUIDO] Todos os PDFs de Pratica 3 e 5 atualizados!
echo ========================================================
pause
