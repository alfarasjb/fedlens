# FedLens

**Run `/streamlit-stack` to load the full Streamlit stack context before starting work.**

## This Repo

**Description**: Analyzes Fed sentiment with embeddings and cosine similarity vs a trained dataset.

**Type**: Streamlit + Quant
**Phase**: n/a

## Commands

Use the Makefile for all commands.

## Key File Locations

- **app.py** — Main Streamlit entry point
- **pages/** — Multi-page Streamlit app pages
- **src/signals/** — Signal generation logic
- **src/viz/** — Visualization helpers
- **src/data/** — Data loading and preprocessing
- **models/** — Trained models and artifacts

## New Pattern References

When implementing new patterns, refer to:

- **Model example**: @D:\Files\Repositories\General\Quant\Fed-Thing\model.ipynb

## Project Context

(To be added)

---

**Before PRs**: Use the quant-validator agent to check for data leakage and methodology errors.
