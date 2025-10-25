#!/bin/bash
# TK Reports Setup Script

echo "========================================="
echo "   TK Reports - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================="
echo "   ✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the Flask application:"
echo "     python app.py"
echo "     or"
echo "     flask run --port=5016"
echo ""
echo "  3. Open your browser to:"
echo "     http://127.0.0.1:5016"
echo ""
echo "========================================="
