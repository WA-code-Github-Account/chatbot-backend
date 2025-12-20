***# Simple startup script for the RAG System Backend
# This starts the server with graceful fallbacks for missing dependencies

import os
import sys
from contextlib import redirect_stderr
import io

print("Starting RAG System Backend Server...")

# Set environment variable to use SQLite
os.environ["USE_SQLITE"] = "true"

try:
    from fastapi import FastAPI
    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ Failed to import FastAPI: {e}")
    sys.exit(1)

# Create a basic app with minimal routes
app = FastAPI(title="RAG System API - Simplified", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "RAG System Backend is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "RAG System API"}

@app.get("/api/v1/test")
async def test_api():
    return {"status": "API endpoint reachable", "message": "Basic functionality working"}

print("✓ FastAPI app created successfully")

# Try to include the main API routes, but gracefully handle if dependencies are missing
try:
    from src.api.v1.router import api_router
    app.include_router(api_router, prefix="/api/v1")
    print("✓ API routes loaded successfully")
except Exception as e:
    print(f"⚠ Could not load full API routes due to missing dependencies: {e}")
    print("  Running with minimal functionality...")

# For serving the application
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting server...")
    print("🌐 Access the API at: http://0.0.0.0:8000")
    print("🌐 API documentation at: http://0.0.0.0:8000/docs")
    print("💡 Press Ctrl+C to stop the server\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload in production
    )***
