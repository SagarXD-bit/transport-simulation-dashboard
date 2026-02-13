@echo off
title 🚀 Transport Simulation Dashboard - Sagar Rawat
color 0A

echo ===============================================
echo       TRANSPORT SIMULATION PROJECT - DEMO
echo ===============================================
echo.
echo  Developer : Sagar Rawat
echo  Description: Local web dashboard to control
echo               and monitor transport_sim.py
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH!
    echo Please install Python 3 and add it to your PATH.
    pause
    exit /b
)

REM Start Flask app in a new minimized window
echo [INFO] Starting Flask Dashboard...
start /MIN cmd /c "python app.py"

REM Wait a moment for server to initialize
timeout /t 3 >nul

REM Open default web browser
echo [INFO] Opening dashboard in default browser...
start http://127.0.0.1:5000

echo.
echo [SUCCESS] Dashboard started successfully!
echo Press CTRL+C in the Flask window to stop the server.
echo ===============================================
pause
