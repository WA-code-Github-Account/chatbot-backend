from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from src.api.v1.router import api_router
from src.middleware.error_handler import setup_error_handlers, LoggingMiddleware
from src.utils.load_book_content import run_document_loading
import uvicorn
import os
import threading


def create_app():
    """Create and configure the FastAPI application"""

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0"
    )

    # CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=["*"],
    )

    # Error handlers
    setup_error_handlers(app)

    # Load book documents on startup (in a separate thread to not block startup)
    @app.on_event("startup")
    async def startup_event():
        print("Loading book content into RAG system...")
        # Run document loading in a separate thread
        thread = threading.Thread(target=run_document_loading)
        thread.start()
        print("Document loading started in background...")

    # Optional logging middleware
    # app.add_middleware(LoggingMiddleware)

    # Include API routes
    try:
        app.include_router(api_router, prefix="/api/v1")
    except Exception as e:
        print(f"Warning: Could not load API routes: {e}")

        @app.get("/api/v1/test")
        async def test_endpoint():
            return {"message": "API routes not loaded due to dependency issues"}

    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "RAG System API"}

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
