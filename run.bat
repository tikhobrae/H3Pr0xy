@echo off
setlocal

set VENV_PATH=venv\Scripts\activate.bat

if exist %VENV_PATH% (
    echo Activating Python virtual environment...
    call %VENV_PATH%
) else (
    echo Python virtual environment not found. Please set up your environment first.
    exit /b 1
)

set TARGET_DIR=src\GoScanner
pushd %TARGET_DIR%
if %errorlevel% neq 0 (
    echo Directory not found: %TARGET_DIR%
    exit /b 1
)

echo Running Go script...
go run run.go

popd
