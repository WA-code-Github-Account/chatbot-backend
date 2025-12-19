#!/usr/bin/env python3
"""
Script to run the RAG System backend server
"""
import os
import sys
import subprocess
from pathlib import Path

def run_server():
    # Change to the backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("Starting RAG System backend server...")
    print("Server will be available at: http://0.0.0.0:8000")
    print("API documentation will be available at: http://0.0.0.0:8000/docs")
    
    # Run the uvicorn server
    try:
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        if result.returncode != 0:
            print(f"Server exited with code: {result.returncode}")
        else:
            print("Server stopped")
            
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    run_server()