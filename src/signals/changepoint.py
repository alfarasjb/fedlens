"""Change point detection using PELT

FUTURE FEATURE: Detects regime changes in hawk-dove score time series.
Not implemented in MVP - coming soon.
"""
import numpy as np
from typing import List


def detect_change_points(
    scores: np.ndarray,
    penalty: int = 10,
    model: str = "rbf"
) -> List[int]:
    """Detect change points using PELT algorithm

    Args:
        scores: Time series of hawk-dove scores
        penalty: PELT penalty parameter (higher = fewer change points)
            - low: pen=5
            - medium: pen=10
            - high: pen=20
        model: Ruptures cost model (default: "rbf")

    Returns:
        List of change point indices
    """
    # TODO: Implement PELT via ruptures library
    # import ruptures as rpt
    # algo = rpt.Pelt(model=model).fit(scores)
    # result = algo.predict(pen=penalty)
    return []


def get_penalty_from_sensitivity(sensitivity: str) -> int:
    """Map sensitivity label to PELT penalty value

    Args:
        sensitivity: "Low", "Medium", or "High"

    Returns:
        Penalty parameter
    """
    mapping = {
        "Low": 5,
        "Medium": 10,
        "High": 20
    }
    return mapping.get(sensitivity, 10)
