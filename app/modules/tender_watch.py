"""Tender-Watch module

Detects possible bid rigging / cartelization by measuring textual similarity
between multiple tender / bid PDF documents.

Pipeline:
- Parse PDF text using pdfplumber.
- Encode each document using a Transformer (DistilBERT) to get dense vectors.
- Compute cosine similarity between all pairs of bids.
- If similarity > threshold (e.g. 0.95), flag as "Collusion Risk".

This is a simplified but explainable approach suitable for a hackathon:
- We use mean-pooled token embeddings from DistilBERT as document embeddings.
- In production you would likely fine-tune a sentence-transformer.
"""

from typing import List, Dict, Any
from io import BytesIO

import pdfplumber
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


# Load a lightweight Transformer once at import time so repeated API calls are fast.
_TOKENIZER = AutoTokenizer.from_pretrained("distilbert-base-uncased")
_MODEL = AutoModel.from_pretrained("distilbert-base-uncased")
_EMBED_DIM = _MODEL.config.hidden_size


def _extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF file represented as bytes.

    We iterate over each page and concatenate the extracted text.
    """

    pages_text: List[str] = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text() or "")
    return "\n".join(pages_text)


def _embed_text(text: str) -> np.ndarray:
    """Encode a document into a fixed-size vector using DistilBERT.

    Steps:
    - Tokenize the input text.
    - Run it through DistilBERT to get token-level embeddings.
    - Apply mean pooling over tokens, respecting the attention mask.
    """

    if not text.strip():
        return np.zeros((_EMBED_DIM,), dtype=float)

    inputs = _TOKENIZER(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )
    with torch.no_grad():
        outputs = _MODEL(**inputs)
        token_embeddings = outputs.last_hidden_state  # (1, seq_len, dim)

    attention_mask = inputs["attention_mask"].unsqueeze(-1)  # (1, seq_len, 1)
    masked_embeddings = token_embeddings * attention_mask
    sum_embeddings = masked_embeddings.sum(dim=1)  # (1, dim)
    token_counts = attention_mask.sum(dim=1).clamp(min=1)  # avoid division by zero
    mean_pooled = (sum_embeddings / token_counts).squeeze(0)  # (dim,)

    return mean_pooled.cpu().numpy()


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors using PyTorch."""

    a_t = torch.from_numpy(a).float().unsqueeze(0)
    b_t = torch.from_numpy(b).float().unsqueeze(0)
    if a_t.norm().item() == 0 or b_t.norm().item() == 0:
        return 0.0
    return float(F.cosine_similarity(a_t, b_t).item())


def analyze_pdfs(pdf_bytes_list: List[bytes], similarity_threshold: float = 0.95) -> Dict[str, Any]:
    """Analyze a list of PDF bid documents and flag highly similar pairs.

    Args:
        pdf_bytes_list: Raw bytes of uploaded PDFs (each one bid document).
        similarity_threshold: Cosine similarity above which we flag collusion risk.

    Returns:
        A JSON-serializable dict containing:
        - total_documents
        - flagged_pairs: list of dicts with (i, j, similarity, collusion_risk, notes)
    """

    texts: List[str] = []
    embeddings: List[np.ndarray] = []

    # Step 1: parse PDFs and embed each document
    for pdf_bytes in pdf_bytes_list:
        text = _extract_text_from_pdf_bytes(pdf_bytes)
        texts.append(text)
        embeddings.append(_embed_text(text))

    n_docs = len(embeddings)
    flagged = []

    # Step 2: pairwise similarity comparison
    for i in range(n_docs):
        for j in range(i + 1, n_docs):
            sim = _cosine_similarity(embeddings[i], embeddings[j])
            if sim >= similarity_threshold:
                flagged.append(
                    {
                        "doc_indices": [i, j],
                        "similarity": sim,
                        "collusion_risk": True,
                        "reason": "Textual similarity above threshold; possible collusion / bid-rigging.",
                    }
                )

    return {
        "total_documents": n_docs,
        "similarity_threshold": similarity_threshold,
        "flagged_pairs": flagged,
    }

