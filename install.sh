#!/bin/bash
# Alternative Lifestyle AI - Linux/Mac Install Script

echo "========================================"
echo "  Alternative Lifestyle AI Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.9+ first."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate and install
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "To run the AI:"
echo "  source venv/bin/activate"
echo "  python cli.py -i"
echo ""
echo "Or:"
echo "  streamlit run web_interface.py"
echo "  uvicorn api:app --reload"
echo ""