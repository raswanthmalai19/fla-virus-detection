#!/bin/bash

# Virus Detection System - Startup Script

echo "============================================================"
echo "🛡️  Virus Signature Detection System - Starting Server"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check dependencies
echo "✓ Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask not installed. Installing..."
    pip3 install -r requirements.txt
fi

python3 -c "import flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask-CORS not installed. Installing..."
    pip3 install -r requirements.txt
fi

echo "✓ All dependencies installed"
echo ""

# Start server
echo "🚀 Starting backend server..."
echo "📊 Dashboard will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 backend/app.py
