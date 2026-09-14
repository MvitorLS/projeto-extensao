@echo off
chcp 65001 > nul
echo ========================================================
echo   Compilando Proposta e Relatorio da Pratica 3...
echo ========================================================
cd /d "%~dp0\Pratica 3"
call compilar_tudo.bat
