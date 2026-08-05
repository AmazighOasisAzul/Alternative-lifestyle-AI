@echo off
cd /d "%~dp0"

echo ========================================
echo  Alternative Lifestyle AI - Setup
echo ========================================

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing / updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Starting AI (CLI)...
python cli.py -i

pause