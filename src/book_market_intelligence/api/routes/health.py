"""
Health check and system diagnostics routes.
"""

from fastapi import APIRouter
from book_market_intelligence.api.schemas import HealthResponse
from book_market_intelligence.config.settings import settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version="2.0.0",
        environment=settings.APP_ENV,
        service="book-market-intelligence-api"
    )


@router.get("/")
def root_endpoint() -> HealthResponse:
    return health_check()
