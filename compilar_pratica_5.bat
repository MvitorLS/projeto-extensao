@echo off
chcp 65001 > nul
echo ========================================================
echo   Compilando Proposta e Relatorio da Pratica 5...
echo ========================================================
cd /d "%~dp0\Pratica 5"
call compilar_tudo.bat
