"""Language Drift - Regime Change Detection

How much the Fed's language is changing meeting-to-meeting, and where the regime breaks are.
"""
import streamlit as st
from src.data.loader import load_fomc_data
from src.viz.charts import create_drift_chart

st.title("Language Drift Velocity")
st.caption("Cosine distance between consecutive FOMC meeting embeddings")

# Sidebar controls
with st.sidebar:
    st.header("Chart Controls")

    date_range = st.slider(
        "Date Range",
        min_value=2006,
        max_value=2026,
        value=(2006, 2026)
    )

    show_thresholds = st.checkbox("Show z-score threshold lines", value=True)

# Load data
df = load_fomc_data()

# Main chart - drift velocity
st.subheader("Drift from Previous Meeting")

fig = create_drift_chart(df, show_thresholds=show_thresholds)
st.plotly_chart(fig, use_container_width=True)

# Key finding callout
st.success("""
**Key Finding:** Drift velocity spikes at exactly the three biggest Fed pivots:
2008 GFC, 2020 COVID, 2022 inflation surge.
""")

st.divider()

with st.expander("How is this calculated?"):
    st.write("""
    Drift velocity is the cosine distance between consecutive meeting centroids in 768-dimensional
    embedding space (all-mpnet-base-v2).

    High drift values indicate significant language shifts between FOMC meetings, often corresponding
    to major policy pivots (e.g., 2008 GFC, 2020 COVID, 2022 inflation surge).
    """)
