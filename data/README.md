# Data Files

Pre-computed data files for FedLens.

## Files

| File | Contents | Size estimate |
| --- | --- | --- |
| `fomc_statements.pkl` | date, text, hawk_dove_score, drift, embedding_2d, embedding_3d | ~5MB |
| `hawk_dove_axis.pkl` | 768-dim unit vector | ~6KB |
| `fed_funds_rate.pkl` | date, rate (from FRED) | ~50KB |

## Future Features

| File | Contents | Size estimate |
| --- | --- | --- |
| `change_points.json` | PELT change point detection output | ~2KB |

## Schema

### fomc_statements.pkl
```
- date: datetime64 (FOMC meeting date)
- text: string (full statement text)
- hawk_dove_score: float64 (projection onto hawk-dove axis)
- drift: float64 (cosine distance from previous meeting)
- embedding_2d: object (UMAP 2D coordinates as [x, y])
- embedding_3d: object (UMAP 3D coordinates as [x, y, z])
```

### hawk_dove_axis.pkl
```
np.ndarray of shape (768,) dtype=float32
Unit vector representing hawk-dove axis in embedding space
```

### fed_funds_rate.pkl
```
- date: datetime64
- rate: float64 (Fed funds rate %)
```

## Data Source

All files are pre-computed from notebooks and checked into the repo for deployment to Streamlit Community Cloud.

Raw embeddings (768-dim × 161 statements) are ~500KB as float32 numpy. Can be included in repo or recomputed at startup.
