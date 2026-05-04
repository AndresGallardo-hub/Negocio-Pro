@echo off
title Servidor - Negocio Pro
cd /d "%~dp0"
echo Levantando la persiana del sistema...
start http://127.0.0.1:5000/
venv\Scripts\python.exe run.py
pause