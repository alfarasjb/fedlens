"""Language drift computation

Cosine distance between consecutive meeting embeddings.
"""
import numpy as np
import pandas as pd


def compute_cosine_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute cosine distance between two embeddings

    Args:
        emb1: First embedding (768-dim)
        emb2: Second embedding (768-dim)

    Returns:
        Cosine distance (1 - cosine similarity)
    """
    # TODO: Implement cosine distance
    return 0.0


def compute_drift_series(embeddings: np.ndarray) -> np.ndarray:
    """Compute drift from previous meeting for all meetings

    Args:
        embeddings: Array of shape (n_meetings, 768)

    Returns:
        Array of drift scores (first element is NaN)
    """
    # TODO: Implement drift computation
    return np.zeros(len(embeddings))


def compute_drift_zscore(drift: pd.Series) -> pd.Series:
    """Compute z-score of drift values

    Args:
        drift: Drift scores

    Returns:
        Z-scores for identifying significant shifts
    """
    # TODO: Implement drift z-score
    return drift
