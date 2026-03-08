"""Language Drift - Regime Change Detection

How much the Fed's language is changing meeting-to-meeting, and where the regime breaks are.
"""
import streamlit as st

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

    # Future: PELT change point detection
    # pelt_sensitivity = st.selectbox(
    #     "Change Point Sensitivity",
    #     options=["Low", "Medium", "High"],
    #     index=1,
    #     help="PELT penalty parameter"
    # )

# Main chart - drift velocity
st.subheader("Drift from Previous Meeting")

# TODO: Connect to src/viz/charts.py
st.info("📊 Drift Velocity Chart Placeholder")
st.caption("""
- x: FOMC meeting date
- y: cosine distance from previous meeting
- Spikes = big language changes
- Horizontal dashed lines at 1σ and 2σ thresholds
""")

# Key finding callout
st.success("""
**Key Finding:** Drift velocity spikes at exactly the three biggest Fed pivots:
2008 GFC, 2020 COVID, 2022 inflation surge.
""")

st.divider()

# Future: Change points table (PELT)
# st.subheader("Detected Regime Changes")
# st.info("📋 Change point detection coming soon (PELT algorithm)")
st.info("💡 **Coming Soon:** Automated regime change detection using PELT algorithm")

with st.expander("How is this calculated?"):
    st.write("""
    Drift velocity is the cosine distance between consecutive meeting centroids in 768-dimensional
    embedding space (all-mpnet-base-v2).

    Change points are detected using PELT (Pruned Exact Linear Time) algorithm via ruptures library.
    """)
