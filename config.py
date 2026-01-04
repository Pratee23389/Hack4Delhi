"""
Fiscal-Sentinel Configuration
Advanced Algorithmic Fraud Detection - Hyperparameters for CP-Level Performance
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = DATA_DIR / "samples"
UPLOADS_DIR = DATA_DIR / "uploads"

# ==========================================
# NLP/Vector Space Configuration
# ==========================================
class TenderWatchConfig:
    """Configuration for Tender-Watch NLP Module - Vector Embeddings"""
    
    # Model: all-MiniLM-L6-v2 produces 384-dimensional embeddings
    MODEL_NAME = 'all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION = 384
    
    # Similarity threshold for collusion detection (cosine similarity in high-dimensional space)
    SIMILARITY_THRESHOLD = 0.90  # 90% similarity = suspicious
    CRITICAL_THRESHOLD = 0.96    # 96% similarity = definite fraud
    
    # Vector space optimization
    BATCH_SIZE = 32              # For batch encoding
    MAX_SEQUENCE_LENGTH = 512    # Truncation length


# ==========================================
# Graph Theory Configuration
# ==========================================
class GraphFraudConfig:
    """Configuration for Graph-based Ghost Employee Detection - Connected Components"""
    
    # Connected Components parameters
    MIN_CLIQUE_SIZE = 2          # Minimum size for suspicious cluster
    SUSPICIOUS_CLIQUE_SIZE = 3   # Size that triggers high alert
    
    # Centrality algorithms for Kingpin detection
    CENTRALITY_ALGORITHM = 'betweenness'  # Options: 'degree', 'betweenness', 'closeness'
    TOP_K_SUSPECTS = 5           # Number of top suspects to identify
    
    # Graph density thresholds: Density = 2*E / (V*(V-1)) where E=edges, V=vertices
    LOW_DENSITY_THRESHOLD = 0.3
    HIGH_DENSITY_THRESHOLD = 0.7  # Dense sub-graphs indicate coordinated fraud
    
    # Bipartite graph configuration
    EMPLOYEE_NODE_PREFIX = 'EMP_'
    ATTRIBUTE_NODE_PREFIX = 'ATTR_'


# ==========================================
# Statistical Analysis Configuration
# ==========================================
class PriceGuardConfig:
    """Configuration for Over-Invoicing Detection - Standard Deviation Analysis"""
    
    # Statistical thresholds (Standard Deviation based)
    SIGMA_THRESHOLD = 2.0        # 2σ = 95.45% confidence interval
    CRITICAL_SIGMA = 3.0         # 3σ = 99.73% confidence interval
    
    # Price deviation thresholds
    SUSPICIOUS_INFLATION = 0.50  # 50% over market price
    CRITICAL_INFLATION = 0.75    # 75% over market price
    
    # OCR and text extraction
    OCR_CONFIDENCE_THRESHOLD = 0.70
    MIN_TEXT_LENGTH = 10
    
    # Weighted Levenshtein parameters
    INSERTION_COST = 1.0
    DELETION_COST = 1.0
    SUBSTITUTION_COST = 2.0      # Higher cost for character substitution


# ==========================================
# Fuzzy Matching Configuration
# ==========================================
class WelfareShieldConfig:
    """Configuration for Deceased Beneficiary Detection - Fuzzy String Matching"""
    
    # Fuzzy matching algorithms (handles NP-Hard string alignment)
    ALGORITHM = 'token_sort_ratio'  # Options: 'ratio', 'partial_ratio', 'token_sort_ratio'
    JARO_WINKLER_PREFIX_WEIGHT = 0.1  # Boost for matching prefixes
    
    # Matching thresholds (0-100 scale)
    FUZZY_MATCH_THRESHOLD = 85   # General threshold
    HIGH_CONFIDENCE_THRESHOLD = 95
    
    # Name preprocessing
    NORMALIZE_CASE = True
    REMOVE_PUNCTUATION = True
    REMOVE_TITLES = True         # Remove Mr., Mrs., Dr., etc.
    
    # String alignment complexity optimization
    MAX_STRING_LENGTH = 100      # Performance optimization for NP-Hard problem


# ==========================================
# System-Wide Configuration
# ==========================================
class SystemConfig:
    """Global system configuration for production-level performance"""
    
    # FastAPI settings
    API_TITLE = "Fiscal-Sentinel Defense Systems"
    API_VERSION = "2.0.0"
    API_PORT = 8000
    
    # Performance optimization
    ENABLE_ASYNC = True
    MAX_WORKERS = 4
    REQUEST_TIMEOUT = 30         # seconds
    
    # Logging and monitoring
    LOG_LEVEL = "INFO"
    ENABLE_METRICS = True
    
    # Integrity Score calculation - Weighted combination of all module outputs
    WEIGHTS = {
        'tender_watch': 0.30,
        'graph_fraud': 0.35,     # Highest weight - most reliable
        'price_guard': 0.20,
        'welfare_shield': 0.15
    }
    
    # Overall system thresholds
    SYSTEM_INTEGRITY_SCORE_LOW = 70   # Below this = high fraud risk
    SYSTEM_INTEGRITY_SCORE_HIGH = 90  # Above this = clean


# ==========================================
# Visualization Configuration
# ==========================================
class VisualizationConfig:
    """Configuration for defense dashboard visualizations"""
    
    # Graph visualization
    GRAPH_LAYOUT = 'spring'      # Options: 'spring', 'circular', 'kamada_kawai'
    NODE_SIZE_RANGE = (100, 500) # Min and max node sizes
    EDGE_WIDTH_RANGE = (1, 5)
    
    # Color schemes
    FRAUD_COLOR = '#FF4444'      # Red for fraud
    SUSPICIOUS_COLOR = '#FFA500' # Orange for suspicious
    CLEAN_COLOR = '#44FF44'      # Green for clean
    
    # Heatmap settings
    HEATMAP_COLORSCALE = 'Reds'
    HEATMAP_RESOLUTION = (800, 600)


# ==========================================
# Legacy compatibility
# ==========================================
NEO4J_URI = os.getenv("NEO4J_URI", None)
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
TRANSFORMER_MODEL = TenderWatchConfig.MODEL_NAME
DEFAULT_SIMILARITY_THRESHOLD = TenderWatchConfig.SIMILARITY_THRESHOLD
DEFAULT_PRICE_INFLATION_FACTOR = PriceGuardConfig.SUSPICIOUS_INFLATION + 1
DEFAULT_CLUSTER_SIZE = GraphFraudConfig.SUSPICIOUS_CLIQUE_SIZE
DEFAULT_FUZZY_MATCH_THRESHOLD = WelfareShieldConfig.FUZZY_MATCH_THRESHOLD

# Create directories if they don't exist
for directory in [DATA_DIR, SAMPLE_DATA_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
