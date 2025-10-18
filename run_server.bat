@echo off
REM Virus Detection System - Startup Script for Windows

echo ============================================================
echo Virus Signature Detection System - Starting Server
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Python found
echo.

REM Install dependencies
echo Checking dependencies...
pip install -r requirements.txt
echo.

REM Start server
echo Starting backend server...
echo Dashboard will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python backend/app.py

pause
