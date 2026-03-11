"""Plotly chart builders

All chart creation functions as pure functions. Never use st.write() inside these.
"""
import plotly.graph_objects as go
import pandas as pd


def create_sentiment_timeline(
    df: pd.DataFrame,
    show_fed_funds: bool = False,
    fed_funds_data: pd.Series = None,
    ewm_span: int = 15
) -> go.Figure:
    """Create hawk-dove score timeline chart

    Args:
        df: DataFrame with date, hawk_dove_score columns
        show_fed_funds: Overlay Fed funds rate on secondary axis
        fed_funds_data: Fed funds rate time series (if show_fed_funds=True)
        ewm_span: Exponentially weighted moving average span

    Returns:
        Plotly figure
    """
    # Placeholder implementation
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Calculate EWM smoothed scores
    df['ewm_score'] = df['hawk_dove_score'].ewm(span=ewm_span).mean()

    # Create figure with secondary y-axis if showing fed funds
    from plotly.subplots import make_subplots

    if show_fed_funds and fed_funds_data is not None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    else:
        fig = go.Figure()

    # Primary line - raw hawk-dove scores
    primary_trace = go.Scatter(
        x=df['date'],
        y=df['hawk_dove_score'],
        mode='lines',
        name='Fed Sentiment',
        line=dict(color='steelblue', width=2),
        hovertemplate='%{y:.3f}<extra></extra>'
    )

    if show_fed_funds and fed_funds_data is not None:
        fig.add_trace(primary_trace, secondary_y=False)
    else:
        fig.add_trace(primary_trace)

    # EWM smoothed line (subtle, background)
    ewm_trace = go.Scatter(
        x=df['date'],
        y=df['ewm_score'],
        mode='lines',
        name=f'EWM (span={ewm_span})',
        line=dict(color='lightgray', width=2, dash='dot'),
        opacity=0.5,
        hovertemplate='EWM: %{y:.3f}<extra></extra>'
    )

    if show_fed_funds and fed_funds_data is not None:
        fig.add_trace(ewm_trace, secondary_y=False)
    else:
        fig.add_trace(ewm_trace)

    # Fed funds overlay if requested
    if show_fed_funds and fed_funds_data is not None:
        fig.add_trace(
            go.Scatter(
                x=fed_funds_data.index,
                y=fed_funds_data.values,
                mode='lines',
                name='Fed Funds Rate',
                line=dict(color='coral', width=1.5, dash='dot'),
                opacity=0.7
            ),
            secondary_y=True
        )

        fig.update_yaxes(title_text="Fed Sentiment", secondary_y=False)
        fig.update_yaxes(title_text="Fed Funds Rate (%)", secondary_y=True)
    else:
        fig.update_layout(yaxis_title="Fed Sentiment")

    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title="Fed Sentiment Over Time",
        xaxis_title="Date",
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_drift_chart(
    df: pd.DataFrame,
    show_thresholds: bool = True
) -> go.Figure:
    """Create language drift velocity chart

    Args:
        df: DataFrame with date, drift columns
        show_thresholds: Show 1σ and 2σ threshold lines

    Returns:
        Plotly figure
    """
    # Placeholder implementation
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    import numpy as np

    fig = go.Figure()

    # Drift line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['drift'],
        mode='lines+markers',
        name='Drift',
        line=dict(color='coral', width=2),
        marker=dict(size=5),
        fill='tozeroy',
        fillcolor='rgba(255, 127, 80, 0.1)'
    ))

    # Threshold lines if requested
    if show_thresholds:
        drift_clean = df['drift'].replace(0, np.nan).dropna()
        if len(drift_clean) > 0:
            mean = drift_clean.mean()
            std = drift_clean.std()

            fig.add_hline(y=mean + std, line_dash="dash", line_color="orange",
                         opacity=0.5, annotation_text="1σ")
            fig.add_hline(y=mean + 2*std, line_dash="dash", line_color="red",
                         opacity=0.5, annotation_text="2σ")

    fig.update_layout(
        title="Language Drift Velocity",
        xaxis_title="Date",
        yaxis_title="Cosine Distance",
        height=500,
        hovermode='x unified'
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
    # Placeholder implementation
    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=df['hawk_dove_score'],
        nbinsx=30,
        marker=dict(
            color='lightsteelblue',
            line=dict(color='steelblue', width=1)
        ),
        name='Distribution'
    ))

    # "You are here" marker
    fig.add_vline(
        x=latest_score,
        line_dash="solid",
        line_color="gold",
        line_width=3,
        annotation_text="You are here",
        annotation_position="top"
    )

    # Zero line
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title="Score Distribution",
        xaxis_title="Fed Sentiment",
        yaxis_title="Count",
        height=300,
        showlegend=False
    )

    return fig


def create_mini_sentiment_chart(df: pd.DataFrame, years: int | None = None) -> go.Figure:
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

    # Filter to last N years if provided, otherwise, all data 
    if years is None: 
        recent_df = df 
    else: 
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=years)
        recent_df = df[df['date'] >= cutoff_date].copy()

    fig = go.Figure()

    # Add hawk-dove score line
    fig.add_trace(go.Scatter(
        x=recent_df['date'],
        y=recent_df['hawk_dove_score'],
        mode='lines+markers',
        name='Fed Sentiment',
        line=dict(color='steelblue', width=2),
        marker=dict(size=6)
    ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    # Determine title based on whether years is specified
    if years is None:
        title = "Hawk-Dove Sentiment"
    else:
        title = f"Recent Sentiment (Last {years} Years)"

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Fed Sentiment",
        height=300,
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(fixedrange=True),  # Disable zoom/pan on x-axis
        yaxis=dict(fixedrange=True)   # Disable zoom/pan on y-axis
    )

    return fig
