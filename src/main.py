from fastapi import FastAPI
from config.settings import settings
from src.api.v1.router import api_router
from src.middleware.error_handler import setup_error_handlers, LoggingMiddleware
import uvicorn


def create_app():
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0"
    )

    # Set up error handlers
    setup_error_handlers(app)

    # Add middleware
    # Add middleware
    #app.add_middleware(LoggingMiddleware)


    # Include API routes
    try:
        app.include_router(api_router, prefix="/api/v1")
    except Exception as e:
        print(f"Warning: Could not load API routes: {e}")
        # Still add a basic route for testing
        @app.get("/api/v1/test")
        async def test_endpoint():
            return {"message": "API routes not loaded due to dependency issues"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "RAG System API"}

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )