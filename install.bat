@echo off
REM Alternative Lifestyle AI - Windows Install Script

@echo ========================================
@echo   Alternative Lifestyle AI Setup
@echo ========================================
@echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.9+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment
@echo Creating virtual environment...
python -m venv venv

REM Activate and install
@echo Installing dependencies...
call venvScriptsactivate
pip install -r requirements.txt

@echo.
@echo ========================================
@echo   Setup Complete!
@echo ========================================
@echo.
@echo To run the AI:
@echo   call venvScriptsactivate
@echo   python cli.py -i
@echo.
@echo Or:
@echo   streamlit run web_interface.py
@echo   uvicorn api:app --reload
@echo.
pause