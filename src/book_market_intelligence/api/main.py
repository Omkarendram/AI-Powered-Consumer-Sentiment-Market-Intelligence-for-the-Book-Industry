"""
FastAPI application factory and middleware configuration.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from book_market_intelligence.api.routes import (
    health_router,
    rag_router,
    sentiment_router,
    analytics_router
)
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger


def create_app() -> FastAPI:
    """Creates and configures the production FastAPI instance."""
    app = FastAPI(
        title="AI-Powered Book Market Intelligence API",
        description=(
            "Enterprise REST API for customer sentiment analysis, aspect extraction, "
            "and Retrieval-Augmented Generation (RAG) market intelligence."
        ),
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled API error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error occurred.", "path": request.url.path}
        )

    # Include routers
    app.include_router(health_router)
    app.include_router(rag_router)
    app.include_router(sentiment_router)
    app.include_router(analytics_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("book_market_intelligence.api.main:app", host=settings.HOST, port=settings.PORT, reload=settings.APP_DEBUG)
