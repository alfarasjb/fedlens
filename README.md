# FedLens

Interactive Streamlit dashboard tracking Fed sentiment through embeddings and cosine similarity analysis.

**Thesis:** Language shifts between FOMC meetings lead actual rate decisions by 1–2 meetings. This dashboard tracks that drift in real time.

## What It Demonstrates

- Hawk-dove sentiment scoring via geometric projection onto learned axis
- Language drift detection between consecutive FOMC meetings
- Change point detection (PELT) for regime identification
- Lead/lag correlation analysis (EWM z-score at lag +1, r = 0.47)
- 3D UMAP trajectory visualization

## Stack

- Python 3.11
- Streamlit (multi-page navigation)
- Plotly (interactive charts)
- sentence-transformers (`all-mpnet-base-v2`)
- ruptures (PELT change point detection)

## Setup

```bash
make install
```

## Run Locally

```bash
make run
```

Or directly:
```bash
streamlit run app.py
```

App will open at `http://localhost:8501`

## Project Structure

```
app.py                    # Entry point + st.navigation
pages/
  overview.py             # Key findings + alert banner
  sentiment.py            # Hawk-dove score timeline
  drift.py                # Language drift velocity + change points
  trajectory.py           # 3D UMAP trajectory
  methodology.py          # How it works + links
src/
  data/loader.py          # Load + cache FOMC data
  signals/sentiment.py    # Hawk-dove projection (pure functions)
  signals/drift.py        # Cosine drift computation
  signals/changepoint.py  # PELT change point detection
  viz/charts.py           # All Plotly chart builders
data/
  fomc_statements.pkl     # Embedded + scored statements
  hawk_dove_axis.pkl      # Pre-trained hawk-dove axis
  fed_funds_rate.pkl      # Fed funds rate from FRED
```

## Data Files

All data files are pre-computed and should be checked into the repo before deployment. See `data/README.md` for schemas.

## Deployment

Deploy to Streamlit Community Cloud:
1. Connect GitHub repo
2. Select `app.py` as entry point
3. Deploy (cold start ~30s with sentence-transformers)

## Related

- Medium article: (link when published)
- Research notebook: `model.ipynb`
- Trillion Dollar Words dataset (ACL 2023)
