"""
Tender-Watch Module
Detects bid rigging and collusion by comparing tender document similarity
"""

import pdfplumber
from io import BytesIO
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF bytes"""
    text_pages = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)


def analyze_tenders(pdf_files_bytes):
    """
    Analyze multiple tender PDFs for collusion
    Returns list of flagged pairs with high similarity
    """
    # Extract text from all PDFs
    texts = [extract_text_from_pdf(pdf_bytes) for pdf_bytes in pdf_files_bytes]
    
    # Generate embeddings
    embeddings = model.encode(texts)
    
    # Calculate pairwise cosine similarity
    similarity_matrix = cosine_similarity(embeddings)
    
    # Find pairs with similarity > 90%
    flagged_pairs = []
    n = len(texts)
    
    for i in range(n):
        for j in range(i + 1, n):
            similarity_score = float(similarity_matrix[i][j]) * 100  # Convert to percentage
            if similarity_score > 90:
                flagged_pairs.append({
                    'doc_1': i,
                    'doc_2': j,
                    'similarity': round(similarity_score, 2),
                    'status': 'COLLUSION DETECTED',
                    'reason': f'Documents {i+1} and {j+1} are {similarity_score:.1f}% similar'
                })
    
    return {
        'total_documents': n,
        'flagged_pairs': flagged_pairs,
        'status': 'WARNING' if flagged_pairs else 'CLEAR'
    }
