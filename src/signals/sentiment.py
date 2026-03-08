"""Hawk-dove sentiment scoring

Pure functions for computing hawk-dove projections and smoothing.
"""
import pandas as pd
import numpy as np


def compute_hawk_dove_score(embedding: np.ndarray, axis: np.ndarray) -> float:
    """Project embedding onto hawk-dove axis

    Args:
        embedding: 768-dim sentence embedding
        axis: 768-dim hawk-dove axis (unit vector)

    Returns:
        Projection score (positive = hawkish, negative = dovish)
    """
    # TODO: Implement geometric projection
    return 0.0


def compute_ewm_scores(scores: pd.Series, span: int = 15) -> pd.Series:
    """Compute exponentially weighted moving average of scores

    Args:
        scores: Raw hawk-dove scores
        span: EWM span parameter (default: 15)

    Returns:
        Smoothed scores
    """
    # TODO: Implement EWM smoothing
    return scores


def compute_ewm_zscore(scores: pd.Series, span: int = 15) -> pd.Series:
    """Compute EWM z-score for lead/lag analysis

    Args:
        scores: Raw hawk-dove scores
        span: EWM span parameter

    Returns:
        Z-scores (normalized deviations)
    """
    # TODO: Implement z-score computation
    return pd.Series()

