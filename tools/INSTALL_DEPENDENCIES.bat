@echo off
REM Install all required dependencies for Invoice Management System

echo ========================================
echo Installing Required Dependencies...
echo ========================================
echo.

echo Step 1: Installing Flask...
python -m pip install flask --upgrade
if errorlevel 1 goto error

echo.
echo Step 2: Installing Flask-Login...
python -m pip install flask-login --upgrade
if errorlevel 1 goto error

echo.
echo Step 3: Installing ReportLab...
python -m pip install reportlab --upgrade
if errorlevel 1 goto error

echo.
echo Step 4: Installing QRCode with Pillow...
python -m pip install qrcode[pil] --upgrade
if errorlevel 1 goto error

echo.
echo ========================================
echo ✅ All dependencies installed successfully!
echo ========================================
echo.
echo You can now run: python app.py
echo.
pause
exit /b 0

:error
echo.
echo ❌ Installation failed!
echo Please check the error messages above.
pause
exit /b 1
