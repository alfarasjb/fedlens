"""Fed Communications Analyzer - Interactive Dashboard"""
import streamlit as st

st.set_page_config(
    page_title="Fed Communications Analyzer",
    page_icon="🏛️",
    layout="wide"
)

# Multi-page navigation
pg = st.navigation([
    st.Page("pages/overview.py", title="Overview", icon="🏛️"),
    st.Page("pages/sentiment.py", title="Sentiment Timeline", icon="📈"),
    st.Page("pages/drift.py", title="Language Drift", icon="📊"),
    st.Page("pages/trajectory.py", title="3D Trajectory", icon="🌐"),
    st.Page("pages/methodology.py", title="Methodology", icon="📖"),
])

pg.run()
