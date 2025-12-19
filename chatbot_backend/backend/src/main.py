from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from src.api.v1.router import api_router
from src.middleware.error_handler import setup_error_handlers, LoggingMiddleware
import uvicorn
import os

def create_app():
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0"
    )

    # CORS settings - allow requests from your frontend domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=["*"],
        # expose_headers=["Access-Control-Allow-Origin"]
    )

    # Set up error handlers
    setup_error_handlers(app)

    # Add middleware if needed
    # app.add_middleware(LoggingMiddleware)

    # Include API routes
    try:
        app.include_router(api_router, prefix="/api/v1")
    except Exception as e:
        print(f"Warning: Could not load API routes: {e}")
        # Add a simple test route if API routes fail
        @app.get("/api/v1/test")
        async def test_endpoint():
            return {"message": "API routes not loaded due to dependency issues"}

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "RAG System API"}

    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Use Railway's PORT environment variable if available
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
