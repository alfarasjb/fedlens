"""Overview - Landing Page

Key findings surfaced immediately. Visitors understand the thesis within 30 seconds.
"""
import streamlit as st
import numpy as np
import pandas as pd
from src.data.loader import load_fomc_data
from src.data.updater import update_fomc_data, reprocess_existing_data, get_last_update_time
from src.viz.charts import create_mini_sentiment_chart

st.title("FedLens")
st.caption("Language shifts between FOMC meetings lead actual rate decisions by 1–2 meetings. This dashboard tracks that drift in real time.")

# Sidebar - Data Update Controls
with st.sidebar:
    st.header("Data Management")

    last_update = get_last_update_time()
    st.caption(f"Last updated: {last_update}")

    # Option 1: Fetch new data from Fed website
    if st.button("🌐 Fetch New Statements", type="primary", use_container_width=True):
        with st.spinner("Fetching latest FOMC statements from Fed website..."):
            try:
                num_new, message = update_fomc_data()

                if num_new > 0:
                    st.success(message)
                    st.info("💡 Refresh the page (F5) to see updated data")
                    # Clear Streamlit cache to reload data
                    st.cache_data.clear()
                else:
                    st.info(message)
            except Exception as e:
                st.error(f"Fetch failed: {str(e)}")
                st.caption("Try 'Reprocess Data' if you've manually updated the CSV")

    # Option 2: Reprocess existing data
    if st.button("🔄 Reprocess Data", use_container_width=True):
        with st.spinner("Recalculating embeddings and scores..."):
            try:
                success, message = reprocess_existing_data()

                if success:
                    st.success(message)
                    st.info("💡 Refresh the page (F5) to see updated calculations")
                    st.cache_data.clear()
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Reprocess failed: {str(e)}")

    st.divider()

    with st.expander("ℹ️ About Updates"):
        st.caption("""
        **Fetch New Statements**: Downloads new FOMC statement PDFs
        from the Federal Reserve website using predictable URLs
        (pattern: monetary{YYYYMMDD}a1.pdf). Checks recent meeting
        dates and adds any new statements found.

        **Reprocess Data**: Recalculates embeddings and scores from
        the existing CSV file. Use this if you've manually added
        statements to fomc_statements.csv.

        After updating, refresh the page (F5) to reload the data.
        """)

st.divider()

# Load data
df = load_fomc_data()
df['date'] = pd.to_datetime(df['date'])  # Ensure datetime
latest = df.iloc[-1]
previous = df.iloc[-2]

# Alert banner - latest statement assessment
# Drop NaN/zeros for drift statistics
drift_clean = df['drift'].replace(0, np.nan).dropna()
drift_mean = drift_clean.mean()
drift_std = drift_clean.std()
z_score = (latest['drift'] - drift_mean) / drift_std if drift_std > 0 else 0

if z_score > 2:
    st.error("🚨 SIGNIFICANT TONE SHIFT DETECTED")
elif z_score > 1:
    st.warning("⚠️ Notable language change")
else:
    st.success("✅ Business as usual")

st.divider()

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    score = latest['hawk_dove_score']
    sentiment = "Hawkish" if score > 0 else "Dovish"
    st.metric("Latest Fed Sentiment", f"{score:+.3f}", delta=sentiment)

with col2:
    drift_val = latest['drift']
    # Show z-score as additional info, not delta (delta implies direction)
    st.metric("Drift from Last Meeting", f"{drift_val:.3f}")
    if abs(z_score) < 0.1:
        st.caption("(within normal range)")
    else:
        st.caption(f"Z-score: {z_score:+.2f}σ")

with col3:
    latest_date = latest['date'].strftime("%b %Y")
    st.metric("Latest Meeting", latest_date)

with col4:
    st.metric("Total Meetings", len(df))

st.divider()

# Mini sentiment chart - last 3 years
st.subheader("Recent Sentiment Trend")
st.caption("Last 3 years. Full timeline on Sentiment page.")

fig = create_mini_sentiment_chart(df, years=3)
st.plotly_chart(fig, use_container_width=True)

with st.expander("💡 One-line thesis"):
    st.write("""
    Language shifts between FOMC meetings lead actual rate decisions by 1–2 meetings.
    This dashboard tracks that drift in real time.
    """)
