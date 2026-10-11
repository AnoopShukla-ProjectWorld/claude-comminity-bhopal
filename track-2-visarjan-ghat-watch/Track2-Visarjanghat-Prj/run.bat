@echo off
chcp 65001 >nul
title Bhopal Impact Lab 2026 - Visarjan Ghat Watch Setup & Launcher
color 0A

echo ===============================================================================
echo     BHOPAL IMPACT LAB 2026 · TRACK 2: VISARJAN GHAT WATCH
echo     Idol Immersion Water Quality Intelligence System (Bhopal Municipal Corp)
echo ===============================================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your system PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Python environment...
python --version

:: 2. Check or create virtual environment (venv)
if not exist "venv" (
    echo [2/4] Creating virtual environment (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [WARNING] Could not create virtual environment. Installing packages globally...
        goto install_global
    )
)

:install_venv
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo [3/4] Installing / Updating required packages from requirements.txt...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
goto launch_server

:install_global
echo [3/4] Installing required packages globally...
pip install -r requirements.txt

:launch_server
echo [4/4] Running system self-diagnostics...
python test_system.py
if %errorlevel% neq 0 (
    echo [WARNING] Some diagnostics failed, but attempting to start the server...
)

echo.
echo ===============================================================================
echo     SUCCESS! System is starting on: http://localhost:5000
echo     Opening your default web browser automatically...
echo     (To stop the application, close this window or press Ctrl + C)
echo ===============================================================================
echo.

:: Automatically open browser after 2 seconds
start "" http://localhost:5000

:: Start Flask server
python app.py

pause
