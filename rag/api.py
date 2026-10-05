"""
Backward compatibility layer for FastAPI RAG endpoint.
Delegates to book_market_intelligence.api.main.app.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.api.main import app
from book_market_intelligence.config.settings import settings

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", settings.PORT))
    uvicorn.run("book_market_intelligence.api.main:app", host=settings.HOST, port=port, reload=True)
