"""FedLens Data Loader

Loads pre-computed FOMC data and model artifacts with Streamlit caching.
"""
import os
import pickle
from typing import Any

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from fredapi import Fred 

@st.cache_resource
def load_embedding_model() -> SentenceTransformer:
    """Load sentence transformer model (heavy, loaded once)"""
    return SentenceTransformer("all-mpnet-base-v2")


@st.cache_resource
def load_hawk_dove_axis() -> np.ndarray:
    """Load pre-computed hawk-dove axis (768-dim unit vector)"""
    return load_pickle("data/hawk_dove_axis.pkl")


@st.cache_data
def load_fomc_data() -> pd.DataFrame:
    """Load FOMC statements with embeddings and scores

    Returns:
        DataFrame with columns:
            - date: FOMC meeting date
            - text: statement text
            - hawk_dove_score: projection onto hawk-dove axis
            - drift: cosine distance from previous meeting
            - embedding_2d: UMAP 2D coordinates
            - embedding_3d: UMAP 3D coordinates
    """
    df = load_pickle("data/fomc_data.pkl")

    # Use 'drifts' column if exists, otherwise create placeholder
    if 'drifts' in df.columns and 'drift' not in df.columns:
        df['drift'] = df['drifts']
    elif 'drift' not in df.columns:
        df['drift'] = 0.0  # Placeholder

    return df


@st.cache_data
def load_fed_funds_rate(start: str = "2006-01-01", end: str = "2026-03-01") -> pd.DataFrame:
    """Load Fed funds rate time series from FRED

    Returns:
        DataFrame with columns:
            - date: observation date
            - rate: Fed funds rate
    """
    fred = Fred(api_key=os.getenv("FRED_API_KEY")) 
    dff = fred.get_series("DFF", observation_start=start, observation_end=end)
    dff.name = "fet_funds_rate" 
    dff.index = pd.to_datetime(dff.index)

    return dff  

def load_pickle(file_path: str) -> Any:
    """Load a pickle file

    Args:
        file_path: path to the pickle file

    Returns:
        The loaded object
    """
    with open(file_path, 'rb') as f:
        return pickle.load(f)