#!/bin/bash

VENV_PATH="venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    echo "Activating Python virtual environment..."
    source "$VENV_PATH"
else
    echo "Python virtual environment not found. Please set up your environment first."
    exit 1
fi

TARGET_DIR="src/GoScanner"
cd "$TARGET_DIR" || { echo "Directory not found: $TARGET_DIR"; exit 1; }

echo "Running Go script..."
go run run.go
