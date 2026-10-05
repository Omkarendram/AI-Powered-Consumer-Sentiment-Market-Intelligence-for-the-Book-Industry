"""
Test environment imports verification.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import numpy as np
import requests

try:
    import book_market_intelligence
    print("✓ Enterprise package 'book_market_intelligence' imported successfully.")
except Exception as e:
    print(f"✗ Failed importing package: {e}")

print("✓ Core data science & ingestion libraries verified!")