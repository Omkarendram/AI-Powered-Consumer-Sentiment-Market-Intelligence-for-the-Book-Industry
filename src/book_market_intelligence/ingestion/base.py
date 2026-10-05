"""
Abstract base class for all data ingestion collectors.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import pandas as pd
from book_market_intelligence.core.logging import logger


class BaseCollector(ABC):
    """Base interface for third-party market data scraping and API ingestion."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def collect(self, limit: int = 100) -> pd.DataFrame:
        """Collects raw data records and returns a standardized pandas DataFrame."""
        pass

    def save(self, df: pd.DataFrame, target_path: Path) -> Path:
        """Persists collected DataFrame to target file path."""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(target_path, index=False)
        logger.info(f"[{self.name}] Saved {len(df)} records to {target_path}")
        return target_path
