@echo off
cd /d "%~dp0"
chcp 65001 >nul
powershell -NoProfile -Command "$env:PYTHONIOENCODING='utf-8'; & '.\.venv\Scripts\python.exe' '.\main.py'; exit $LASTEXITCODE"
