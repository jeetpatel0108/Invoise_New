@echo off
REM Reset database and run app

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║          FIXING DATABASE AND STARTING APP                     ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "d:\shree gopal traders"

REM Backup existing database
if exist invoice.db (
    echo [1/3] Backing up existing database...
    copy invoice.db invoice.db.backup >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Could not backup database
        pause
        exit /b 1
    )
    echo       ✅ Backup saved as invoice.db.backup
    
    echo.
    echo [2/3] Removing old database...
    del invoice.db
    if errorlevel 1 (
        echo ERROR: Could not delete database
        pause
        exit /b 1
    )
    echo       ✅ Old database removed
) else (
    echo [1/3] No existing database found
)

echo.
echo [3/3] Starting application...
echo       App will create fresh database...
echo.

python app.py

pause
