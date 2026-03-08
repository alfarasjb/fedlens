"""Methodology - How It Works

Explain what's under the hood. Link to article for depth.
"""
import streamlit as st

st.title("Methodology")
st.caption("How FedLens works")

st.divider()

# Links section
st.subheader("📚 Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📝 Medium Article**")
    st.caption("(link when published)")

with col2:
    st.markdown("**💻 GitHub Repo**")
    st.caption("(link to repo)")

st.divider()

# How it works - collapsible sections
st.subheader("How It Works")

with st.expander("🔤 Embeddings"):
    st.write("""
    **Model:** `all-mpnet-base-v2` from sentence-transformers

    Each FOMC statement is embedded into a 768-dimensional semantic space. Unlike dictionary
    methods (Loughran-McDonald), embeddings capture context, syntax, and subtle tone.

    We compute the centroid embedding per meeting (averaging all sentences in a statement).
    """)

with st.expander("🎯 Hawk-Dove Axis"):
    st.write("""
    **Geometric projection** onto a pre-trained axis derived from labeled Fed communications.

    The axis is computed from anchor phrase centroids in the Trillion Dollar Words dataset (ACL 2023).

    Positive scores = hawkish language, negative = dovish language.

    This is a continuous score, not a binary classification.
    """)

with st.expander("📊 Drift Velocity"):
    st.write("""
    **Cosine distance** between consecutive meeting centroids in the full 768-dimensional space.

    High drift = significant language change between meetings.

    We compute z-scores to identify statistically significant shifts (> 1σ or 2σ).
    """)

with st.expander("🔍 Change Point Detection"):
    st.write("""
    **PELT** (Pruned Exact Linear Time) algorithm via the `ruptures` library.

    Detects regime changes in the hawk-dove score time series.

    Default penalty = 10 (medium sensitivity). Higher penalty = fewer change points.
    """)

with st.expander("❓ Why Not LLM Classification?"):
    st.write("""
    **Advantages of geometric approach:**

    - Continuous scores (not binary labels)
    - No API calls / rate limits
    - Reproducible (deterministic)
    - Interpretable (projection onto learned axis)
    - Fast (no inference latency)

    LLMs are useful for qualitative analysis but not ideal for time-series quantitative work.
    """)

st.divider()

# Baseline comparison
st.subheader("Baseline Comparison")

st.info("📋 Table Placeholder: Geometric vs Loughran-McDonald vs LLM Classification")

st.caption("""
Why embeddings win for this use case:
- Captures context and syntax
- Continuous scoring for time series analysis
- No dictionary maintenance
""")
