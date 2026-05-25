@echo off
REM Cleanup script for Shree Gopal Traders Invoice System

echo Removing __pycache__ directory...
rmdir /s /q __pycache__ 2>nul

echo Removing .env file...
del /q .env 2>nul

echo.
echo Cleanup complete!
echo.
pause
