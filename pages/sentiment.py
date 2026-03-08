"""Sentiment Timeline - The Money Chart

Full hawk-dove score history with rate decisions overlaid.
"""
import streamlit as st

st.title("Hawk-Dove Score Timeline")
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

    show_raw = st.checkbox("Show raw scores", value=True)
    show_fed_funds = st.checkbox("Overlay Fed funds rate", value=True)
    # show_changepoints = st.checkbox("Show change points", value=False)  # Future: PELT

# Main chart placeholder
st.subheader("Hawk-Dove Score Over Time")

# TODO: Connect to src/viz/charts.py
st.info("📊 Hawk-Dove Timeline Chart Placeholder")
st.caption("""
- x: FOMC meeting date
- y: hawk-dove projection score
- Line: EWM smoothed score (primary)
- Dots: raw per-statement scores
- Secondary axis: Fed funds rate (if toggled)
""")

# Key finding callout
st.success("""
**Key Finding:** EWM z-score (span=15) produces a leading signal at lag +1 (r = 0.47) —
language shifts before rates move.
""")

st.divider()

# Score distribution histogram
st.subheader("Score Distribution")
st.info("📊 Distribution histogram placeholder - 'You are here' marker for latest statement")

with st.expander("How is this calculated?"):
    st.write("""
    Hawk-dove scores are computed by projecting each statement's embedding onto a pre-trained
    axis derived from labeled Fed communications (Trillion Dollar Words dataset, ACL 2023).

    Positive scores = hawkish language, negative = dovish language.
    """)
