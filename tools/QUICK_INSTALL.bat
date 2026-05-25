@echo off
REM Direct dependency installer for Invoice System
REM This script installs missing qrcode module

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║          INSTALLING MISSING qrcode MODULE                     ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo.
echo Installing qrcode library...
python -m pip install --upgrade qrcode[pil]

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    echo Please try manually: pip install qrcode[pil]
    pause
    exit /b 1
)

echo.
echo ✅ qrcode library installed successfully!
echo.
echo Installing other required libraries...
python -m pip install flask flask-login reportlab

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          ✅ ALL DEPENDENCIES INSTALLED                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo You can now run:
echo   python app.py
echo.
echo Or use all-in-one startup:
echo   python run_all.py
echo.
pause
