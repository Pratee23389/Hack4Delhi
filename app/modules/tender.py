"""
Tender-Watch Module: NLP-Based Bid Rigging Detection
===============================================================
ALGORITHM: High-Dimensional Vector Space Similarity Analysis
===============================================================

PROBLEM: Detecting collusion in tender documents where bidders 
coordinate their bids to eliminate competition.

APPROACH: Transform text documents into 384-dimensional vectors
and compute cosine similarity in high-dimensional space.

MATHEMATICAL FOUNDATION:
1. Sentence Transformers convert text to embeddings: 
   D → R^384 (where D = document text, R^384 = 384-dim vector space)

2. Cosine Similarity measures angle between vectors:
   cos(θ) = (A·B) / (||A|| × ||B||)
   
3. For normalized vectors: similarity = dot_product(A, B)
   Range: [-1, 1] where 1 = identical, 0 = orthogonal, -1 = opposite

4. High similarity (>90%) indicates suspicious coordination

TIME COMPLEXITY: O(n²) for pairwise comparison of n documents
SPACE COMPLEXITY: O(n × 384) for storing embeddings

WHY THIS WORKS:
- Semantic meaning preserved in vector space
- Synonym replacement still yields high similarity
- Captures context, not just keyword matching
- Robust to paraphrasing attempts
"""

import pdfplumber
from io import BytesIO
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
from pathlib import Path

# Add parent directory for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import TenderWatchConfig

# Load the model once (singleton pattern for performance)
# all-MiniLM-L6-v2: 384-dimensional sentence embeddings, 22.7M parameters
print("Loading SentenceTransformer model (384-dim embeddings)...")
model = SentenceTransformer(TenderWatchConfig.MODEL_NAME)
print(f"✓ Model loaded: {TenderWatchConfig.MODEL_NAME}")


def extract_text_from_pdf(pdf_bytes):
    """
    Extract text from PDF bytes using pdfplumber
    
    Args:
        pdf_bytes: Raw bytes of PDF file
    
    Returns:
        str: Concatenated text from all pages
    """
    text_pages = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)


def analyze_tenders(pdf_files_bytes):
    """
    Analyze multiple tender PDFs for collusion using vector similarity
    
    ALGORITHM STEPS:
    1. Extract text from all PDFs
    2. Generate 384-dimensional embeddings for each document
    3. Compute pairwise cosine similarity matrix
    4. Flag pairs exceeding threshold as suspicious
    
    Args:
        pdf_files_bytes: List of PDF file bytes
    
    Returns:
        dict: Analysis results with flagged pairs and similarity scores
        
    COMPLEXITY:
        Time: O(n²) for n documents (pairwise comparison)
        Space: O(n × 384) for embedding storage
    """
    # STEP 1: Text Extraction
    print(f"Extracting text from {len(pdf_files_bytes)} tender documents...")
    texts = [extract_text_from_pdf(pdf_bytes) for pdf_bytes in pdf_files_bytes]
    
    # STEP 2: Generate Embeddings
    # Transforms text into 384-dimensional vector space
    # Each dimension captures semantic features learned from massive text corpus
    print("Generating 384-dimensional embeddings...")
    embeddings = model.encode(texts, batch_size=TenderWatchConfig.BATCH_SIZE)
    print(f"✓ Generated embeddings shape: {embeddings.shape}")  # Should be (n, 384)
    
    # STEP 3: Compute Cosine Similarity Matrix
    # For normalized vectors, this reduces to dot product
    # Matrix is symmetric with diagonal = 1.0 (self-similarity)
    print("Computing pairwise cosine similarity matrix...")
    similarity_matrix = cosine_similarity(embeddings)
    
    # STEP 4: Identify Suspicious Pairs
    # Threshold-based detection: >90% = suspicious, >96% = critical
    flagged_pairs = []
    n = len(texts)
    
    print(f"Analyzing {n*(n-1)//2} pairwise combinations...")
    for i in range(n):
        for j in range(i + 1, n):
            # Extract similarity score and convert to percentage
            # CRITICAL: Must convert numpy.float32 to Python float for JSON serialization
            similarity_score = float(similarity_matrix[i][j]) * 100
            
            # Determine severity based on threshold
            if similarity_score > TenderWatchConfig.CRITICAL_THRESHOLD * 100:
                status = 'CRITICAL - DEFINITE FRAUD'
                severity = 'CRITICAL'
            elif similarity_score > TenderWatchConfig.SIMILARITY_THRESHOLD * 100:
                status = 'COLLUSION DETECTED'
                severity = 'HIGH'
            else:
                continue  # Below threshold, skip
            
            # Flag this pair
            flagged_pairs.append({
                'doc_1': i,
                'doc_2': j,
                'similarity': round(similarity_score, 2),
                'severity': severity,
                'status': status,
                'reason': f'Documents {i+1} and {j+1} are {similarity_score:.1f}% similar',
                'explanation': 'High cosine similarity in 384-dim vector space indicates coordinated bidding'
            })
            print(f"  🚨 Flagged: Doc {i+1} ↔ Doc {j+1} = {similarity_score:.2f}% similarity")
    
    # Calculate system integrity score
    if flagged_pairs:
        # Lower score for more/higher similarity frauds
        max_similarity = max(pair['similarity'] for pair in flagged_pairs)
        integrity_score = max(0, 100 - (max_similarity - 50))  # Scale: 100=clean, 0=fraud
    else:
        integrity_score = 100
    
    return {
        'total_documents': n,
        'embedding_dimension': TenderWatchConfig.EMBEDDING_DIMENSION,
        'algorithm': 'Cosine Similarity (High-Dimensional Vector Space)',
        'threshold_used': f'{TenderWatchConfig.SIMILARITY_THRESHOLD * 100}%',
        'flagged_pairs': flagged_pairs,
        'status': 'WARNING' if flagged_pairs else 'CLEAR',
        'integrity_score': round(integrity_score, 2)
    }
