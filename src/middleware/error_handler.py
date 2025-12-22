import logging
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
       # await request.body()  # Read the request body
        
        # Log incoming request
        self.logger.info(f"Incoming request: {request.method} {request.url}")
        
        # Process the request
        response = await self.app(scope, receive, send)
        
        # Note: We can't easily log the response here as it's processed asynchronously
        # For now we'll log that the request started
        
        return response


def setup_error_handlers(app):
    """Set up global error handlers for the application"""
    from fastapi.exception_handlers import http_exception_handler
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        logging.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(exc)}
        )

    @app.exception_handler(StarletteHTTPException)
    async def not_found_handler(request: Request, exc: StarletteHTTPException):
        """Handle 404 and other HTTP errors"""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(422)
    async def validation_exception_handler(request: Request, exc):
        """Handle validation errors"""
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "errors": exc.errors()}
        )