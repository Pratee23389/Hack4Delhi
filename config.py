"""Configuration file for Fiscal-Sentinel"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = DATA_DIR / "samples"
UPLOADS_DIR = DATA_DIR / "uploads"

# Neo4j Configuration (optional - only if you want to use Neo4j)
NEO4J_URI = os.getenv("NEO4J_URI", None)  # e.g., "bolt://localhost:7687"
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Model Configuration
TRANSFORMER_MODEL = "distilbert-base-uncased"

# Thresholds
DEFAULT_SIMILARITY_THRESHOLD = 0.95
DEFAULT_PRICE_INFLATION_FACTOR = 2.0
DEFAULT_CLUSTER_SIZE = 5
DEFAULT_FUZZY_MATCH_THRESHOLD = 85

# Create directories if they don't exist
for directory in [DATA_DIR, SAMPLE_DATA_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
