#!/bin/bash
cd "$(dirname "$0")"

echo "========================================"
echo " Alternative Lifestyle AI - Setup (Mac only)"
echo "========================================"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing / updating dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Starting AI (CLI)..."
python cli.py -i