import pickle
import pandas as pd

# Load and inspect
with open("data/fomc_data.pkl", "rb") as f:
    data = pickle.load(f)

print("Type:", type(data))
print("\nShape:", data.shape if hasattr(data, 'shape') else "N/A")
print("\nColumns:", data.columns.tolist() if hasattr(data, 'columns') else "N/A")
print("\nFirst row:")
print(data.head(1) if hasattr(data, 'head') else data)
