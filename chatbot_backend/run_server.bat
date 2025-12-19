@echo off
REM Script to run the RAG System backend
echo Starting RAG System backend...

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Make sure you've run 'python -m venv venv' and 'pip install -r requirements.txt'
)

REM Change to backend directory
cd /d "%~dp0\backend"

REM Run the application
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

pause