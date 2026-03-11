"""Sentiment Timeline - The Money Chart

Full hawk-dove score history with rate decisions overlaid.
"""
import streamlit as st
import pandas as pd
from src.data.loader import load_fomc_data
from src.viz.charts import create_sentiment_timeline, create_score_distribution

st.title("Fed Sentiment Timeline")
st.caption("Language sentiment projected onto hawk-dove axis from Trillion Dollar Words dataset")

# Sidebar controls
with st.sidebar:
    st.header("Chart Controls")

    date_range = st.slider(
        "Date Range",
        min_value=2006,
        max_value=2026,
        value=(2006, 2026)
    )

    ewm_span = st.slider(
        "EWM Span",
        min_value=5,
        max_value=30,
        value=15,
        help="Exponentially weighted moving average smoothing"
    )

    show_fed_funds = st.checkbox("Overlay Fed funds rate", value=True)

# Load data
df = load_fomc_data()

# Filter by date range
df['date'] = pd.to_datetime(df['date'])
df_filtered = df[
    (df['date'].dt.year >= date_range[0]) &
    (df['date'].dt.year <= date_range[1])
].copy()

latest_score = df.iloc[-1]['hawk_dove_score']

# Load Fed funds data if needed
fed_funds_data = None
if show_fed_funds:
    from src.data.loader import load_fed_funds_rate
    fed_funds_data = load_fed_funds_rate()

# Main chart
st.subheader("Fed Sentiment Over Time")

fig = create_sentiment_timeline(
    df_filtered,
    show_fed_funds=show_fed_funds,
    fed_funds_data=fed_funds_data,
    ewm_span=ewm_span
)
st.plotly_chart(fig, use_container_width=True)

# Key finding callout
st.success("""
**Key Finding:** EWM z-score (span=15) produces a leading signal at lag +1 (r = 0.47) —
language shifts before rates move.
""")

st.divider()

# Score distribution histogram
st.subheader("Score Distribution")

fig_dist = create_score_distribution(df, latest_score)
st.plotly_chart(fig_dist, use_container_width=True)

with st.expander("How is this calculated?"):
    st.write("""
    Hawk-dove scores are computed by projecting each statement's embedding onto a pre-trained
    axis derived from labeled Fed communications (Trillion Dollar Words dataset, ACL 2023).

    Positive scores = hawkish language, negative = dovish language.
    """)
