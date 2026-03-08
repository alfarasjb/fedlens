"""Plotly chart builders

All chart creation functions as pure functions. Never use st.write() inside these.
"""
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List


def create_sentiment_timeline(
    df: pd.DataFrame,
    show_raw: bool = True,
    show_fed_funds: bool = False,
    show_changepoints: bool = False,
    changepoint_dates: Optional[List] = None
) -> go.Figure:
    """Create hawk-dove score timeline chart

    Args:
        df: DataFrame with date, hawk_dove_score, ewm_score columns
        show_raw: Show raw scores as scatter
        show_fed_funds: Overlay Fed funds rate on secondary axis
        show_changepoints: Show vertical lines at change points
        changepoint_dates: List of change point dates

    Returns:
        Plotly figure
    """
    # TODO: Implement sentiment timeline chart
    fig = go.Figure()
    fig.update_layout(
        title="Hawk-Dove Score Timeline",
        xaxis_title="Date",
        yaxis_title="Hawk-Dove Score"
    )
    return fig


def create_drift_chart(
    df: pd.DataFrame,
    show_thresholds: bool = True,
    changepoint_dates: Optional[List] = None
) -> go.Figure:
    """Create language drift velocity chart

    Args:
        df: DataFrame with date, drift, drift_zscore columns
        show_thresholds: Show 1σ and 2σ threshold lines
        changepoint_dates: List of change point dates

    Returns:
        Plotly figure
    """
    # TODO: Implement drift chart
    fig = go.Figure()
    fig.update_layout(
        title="Language Drift Velocity",
        xaxis_title="Date",
        yaxis_title="Cosine Distance"
    )
    return fig


def create_trajectory_3d(df: pd.DataFrame) -> go.Figure:
    """Create 3D UMAP trajectory chart

    Args:
        df: DataFrame with date, embedding_3d (x,y,z), drift columns

    Returns:
        Plotly 3D scatter figure
    """
    # TODO: Implement 3D trajectory chart
    fig = go.Figure()
    fig.update_layout(
        title="FOMC Meeting Trajectory (UMAP 3D)",
        scene=dict(
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
            zaxis_title="UMAP 3"
        )
    )
    return fig


def create_trajectory_2d(df: pd.DataFrame, color_by: str = "year") -> go.Figure:
    """Create 2D UMAP trajectory chart

    Args:
        df: DataFrame with date, embedding_2d (x,y) columns
        color_by: Color points by "year", "chair", or "hawk_dove_score"

    Returns:
        Plotly figure
    """
    # TODO: Implement 2D trajectory chart
    fig = go.Figure()
    fig.update_layout(
        title="FOMC Meeting Trajectory (UMAP 2D)",
        xaxis_title="UMAP 1",
        yaxis_title="UMAP 2"
    )
    return fig


def create_score_distribution(df: pd.DataFrame, latest_score: float) -> go.Figure:
    """Create hawk-dove score distribution histogram

    Args:
        df: DataFrame with hawk_dove_score column
        latest_score: Latest statement score for "you are here" marker

    Returns:
        Plotly histogram
    """
    # TODO: Implement distribution histogram
    fig = go.Figure()
    fig.update_layout(
        title="Score Distribution",
        xaxis_title="Hawk-Dove Score",
        yaxis_title="Count"
    )
    return fig


def create_mini_sentiment_chart(df: pd.DataFrame, years: int = 3) -> go.Figure:
    """Create mini hawk-dove chart for overview page

    Args:
        df: DataFrame with date, hawk_dove_score columns
        years: Number of recent years to show

    Returns:
        Plotly figure (compact version)
    """
    # Ensure date column is datetime
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Filter to last N years
    cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=years)
    recent_df = df[df['date'] >= cutoff_date].copy()

    fig = go.Figure()

    # Add hawk-dove score line
    fig.add_trace(go.Scatter(
        x=recent_df['date'],
        y=recent_df['hawk_dove_score'],
        mode='lines+markers',
        name='Hawk-Dove Score',
        line=dict(color='steelblue', width=2),
        marker=dict(size=6)
    ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title=f"Recent Sentiment (Last {years} Years)",
        xaxis_title="Date",
        yaxis_title="Hawk-Dove Score",
        height=300,
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig
