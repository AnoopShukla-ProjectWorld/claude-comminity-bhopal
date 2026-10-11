@echo off
echo ========================================================
echo  Bhopal Visarjan Ghat Watch 2026 - Launcher
echo  Author: Anoop Shukla (Bhopal Impact Lab 2026)
echo ========================================================
echo.
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not detected in your PATH. Please install Python 3.10+
    pause
    exit /b
)

echo Starting Visarjan Ghat Watch Server...
python app.py
pause
