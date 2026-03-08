"""3D Trajectory - The Flight Path (Appendix)

Visually striking visualization. Secondary to quantitative findings.
"""
import streamlit as st

st.title("FOMC Meeting Trajectory")
st.caption("Meeting centroids in UMAP 3D space - the Fed's 'flight path' through language space")

st.warning("""
**Note:** UMAP is for visualization only. All quantitative analysis (hawk-dove scores, drift,
change points) runs in the original 768-dimensional embedding space.
""")

st.divider()

# 3D scatter
st.subheader("3D Trajectory")

# TODO: Connect to src/viz/charts.py
st.info("🌐 3D UMAP Scatter Placeholder")
st.caption("""
- Each point = one FOMC meeting centroid in UMAP 3D space
- Connected by lines in chronological order
- Line segments colored by drift magnitude: grey/blue (low) → orange/red (high)
- Change point meetings: larger marker + annotation
- Interactive: rotate, zoom (Plotly 3D)
""")

st.divider()

# 2D scatter (simpler, more readable)
st.subheader("2D Trajectory (Simplified)")

# TODO: Connect to src/viz/charts.py
st.info("📊 2D UMAP Scatter Placeholder")

# Color options
color_by = st.radio(
    "Color by:",
    options=["Year", "Fed Chair", "Hawk-Dove Score"],
    horizontal=True
)

with st.expander("How is this calculated?"):
    st.write("""
    UMAP (Uniform Manifold Approximation and Projection) reduces the 768-dimensional embeddings
    to 2D/3D for visualization while preserving local and global structure.

    This is purely for visual storytelling - all analysis uses the full embedding space.
    """)
