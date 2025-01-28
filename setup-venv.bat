@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    pause
    exit /b
)
set CURRENT_DIR=%cd%
python -m venv %CURRENT_DIR%\env
call %CURRENT_DIR%\env\Scripts\activate.bat
echo Upgrading pip...
%CURRENT_DIR%\env\Scripts\python.exe -m pip install --upgrade pip
echo Virtual environment created and activated in %CURRENT_DIR%\env
pause
