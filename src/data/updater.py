"""FOMC Data Updater

Fetches new FOMC statements using predictable PDF URLs, generates embeddings,
and recalculates scores.

FOMC statement PDFs follow the pattern:
https://www.federalreserve.gov/monetarypolicy/files/monetary{YYYYMMDD}a1.pdf
"""
import pickle
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, List

import numpy as np
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def get_fomc_meeting_dates() -> List[str]:
    """Get known FOMC meeting dates

    Returns statement release dates (last day of each meeting).
    Update this list annually when the Fed publishes the next year's calendar.

    Source: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

    Returns:
        List of dates in YYYY-MM-DD format
    """
    # Hardcoded FOMC meeting dates (statement release dates)
    # TODO: Update annually with new meeting dates

    fomc_dates = [
        # 2024 meetings (if needed for historical backfill)
        "2024-01-31",
        "2024-03-20",
        "2024-05-01",
        "2024-06-12",
        "2024-07-31",
        "2024-09-18",
        "2024-11-07",
        "2024-12-18",

        # 2025 meetings (if needed for historical backfill)
        "2025-01-29",
        "2025-03-19",
        "2025-05-07",
        "2025-06-18",
        "2025-07-30",
        "2025-09-17",
        "2025-11-06",
        "2025-12-17",

        # 2026 meetings (statement released on last day of meeting)
        "2026-01-28",  # Jan 27-28
        "2026-03-18",  # Mar 17-18
        "2026-04-29",  # Apr 28-29
        "2026-06-17",  # Jun 16-17
        "2026-07-29",  # Jul 28-29
        "2026-09-16",  # Sep 15-16
        "2026-10-28",  # Oct 26-28
        "2026-12-09",  # Dec 8-9
    ]

    return fomc_dates


def download_fomc_statement(date: str) -> Tuple[bool, str]:
    """Download FOMC statement PDF for a given date

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        Tuple of (success, text_content)
    """
    # Convert date to YYYYMMDD format
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_str = date_obj.strftime('%Y%m%d')

    # Construct URL
    url = f"https://www.federalreserve.gov/monetarypolicy/files/monetary{date_str}a1.pdf"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract text from PDF
        text = extract_text_from_pdf_bytes(response.content) 
        print("TEXT FOR DATE ", date)
        print(text) 
        if text and len(text) > 100:  # Sanity check
            return True, text
        else:
            return False, ""

    except requests.HTTPError as e:
        if e.response.status_code == 404: 
            print("404 ")
            return False, ""  # No statement for this date
        else:
            return False, f"HTTP error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        Extracted text
    """
    try:
        import io
        from pypdf import PdfReader

        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)

        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text())

        return '\n'.join(text_parts)

    except ImportError:
        # Fallback: just return indication that PDF processing is unavailable
        return "[PDF text extraction requires pypdf - install with: pip install pypdf]"
    except Exception as e:
        return f"[Error extracting PDF text: {e}]"


def fetch_latest_fomc_statements(existing_dates: set) -> pd.DataFrame:
    """Fetch new FOMC statements not in existing_dates

    Args:
        existing_dates: Set of dates already in the dataset (YYYY-MM-DD format)

    Returns:
        DataFrame with columns: date, source, text
    """
    # Get known FOMC meeting dates
    candidate_dates = get_fomc_meeting_dates()

    new_statements = []

    for date in candidate_dates: 
        print('CHECKING ', date) 
        if date in existing_dates: 
            print("DATE FOUND ", date)
            continue  # Already have this one

        success, text = download_fomc_statement(date)

        if success:
            new_statements.append({
                'date': date,
                'source': 'pdf',
                'text': text
            })
            print(f"✓ Downloaded statement for {date}")
        else:
            # Silently skip dates with no statement 
            print("Failed to fetch for date ", date) 
            print("Text ", text) 
            pass

    return pd.DataFrame(new_statements) if new_statements else pd.DataFrame()


def update_fomc_data(
    existing_csv_path: str | None = None,
    output_pkl_path: str | None = None,
    hawk_dove_axis_path: str | None = None,
) -> Tuple[int, str]:
    """Update FOMC data with latest statements and recalculate scores

    Args:
        existing_csv_path: Path to existing CSV with historical statements (defaults to ../fomc_statements.csv)
        output_pkl_path: Path to save updated pickle file (defaults to data/fomc_data.pkl)
        hawk_dove_axis_path: Path to hawk-dove axis pickle (defaults to data/hawk_dove_axis.pkl)

    Returns:
        Tuple of (num_new_statements, status_message)
    """
    # Set default paths relative to this file
    if existing_csv_path is None:
        existing_csv_path = Path(__file__).parent.parent.parent / "fomc_statements.csv"
    if output_pkl_path is None:
        output_pkl_path = Path(__file__).parent.parent.parent / "data" / "fomc_data.pkl"
    if hawk_dove_axis_path is None:
        hawk_dove_axis_path = Path(__file__).parent.parent.parent / "data" / "hawk_dove_axis.pkl"

    # Convert to Path objects
    existing_csv_path = Path(existing_csv_path)
    output_pkl_path = Path(output_pkl_path)
    hawk_dove_axis_path = Path(hawk_dove_axis_path)

    try:
        # Load existing data
        existing_df = pd.read_csv(existing_csv_path)
        existing_df['date'] = pd.to_datetime(existing_df['date'])
        existing_dates = set(existing_df['date'].dt.strftime('%Y-%m-%d'))

        # Fetch latest statements
        new_statements = fetch_latest_fomc_statements(existing_dates)

        if new_statements.empty:
            return 0, "All statements already up to date"

        # Convert new statements dates to datetime to match existing_df
        new_statements['date'] = pd.to_datetime(new_statements['date'])

        # Combine with existing data
        combined_df = pd.concat([existing_df, new_statements], ignore_index=True)
        combined_df = combined_df.sort_values('date').reset_index(drop=True)

        # Save updated CSV
        combined_df.to_csv(existing_csv_path, index=False)

        # Recalculate embeddings and scores
        model = SentenceTransformer("all-mpnet-base-v2")
        embeddings = model.encode(combined_df['text'].tolist())

        # Load hawk-dove axis
        with open(hawk_dove_axis_path, 'rb') as f:
            hawk_dove_axis = pickle.load(f)

        # Calculate hawk-dove scores
        hawk_dove_scores = embeddings @ hawk_dove_axis

        # Calculate drift (cosine distance from previous meeting)
        drifts = [0.0]  # First meeting has no drift
        for i in range(1, len(embeddings)):
            sim = cosine_similarity([embeddings[i-1]], [embeddings[i]])[0][0]
            drifts.append(1 - sim)

        # Calculate EWM z-scores
        scores_series = pd.Series(hawk_dove_scores)
        ewm = scores_series.ewm(span=15).mean()
        ewm_std = scores_series.ewm(span=15).std()
        hawk_dove_zscores = (hawk_dove_scores - ewm) / ewm_std

        # Create updated DataFrame with all data
        updated_df = combined_df.copy()
        updated_df['hawk_dove_score'] = hawk_dove_scores
        updated_df['hawk_dove_zscore'] = hawk_dove_zscores
        updated_df['drift'] = drifts
        updated_df['embedding'] = [emb.tolist() for emb in embeddings]

        # Save to pickle
        Path(output_pkl_path).parent.mkdir(parents=True, exist_ok=True)
        updated_df.to_pickle(output_pkl_path)

        num_new = len(new_statements)
        latest_date = new_statements['date'].max().strftime('%Y-%m-%d')

        return num_new, f"Successfully added {num_new} new statement(s). Latest: {latest_date}"

    except Exception as e:
        return 0, f"Error updating data: {str(e)}"


def reprocess_existing_data(
    csv_path: str | None = None,
    output_pkl_path: str | None = None,
    hawk_dove_axis_path: str | None = None,
) -> Tuple[bool, str]:
    """Reprocess existing CSV data without fetching new statements

    This is useful when the CSV has been manually updated or
    when you just want to recalculate scores with existing data.

    Args:
        csv_path: Path to CSV with FOMC statements
        output_pkl_path: Path to save updated pickle file
        hawk_dove_axis_path: Path to hawk-dove axis pickle

    Returns:
        Tuple of (success, status_message)
    """
    # Set default paths
    if csv_path is None:
        csv_path = Path(__file__).parent.parent.parent / "fomc_statements.csv"
    if output_pkl_path is None:
        output_pkl_path = Path(__file__).parent.parent.parent / "data" / "fomc_data.pkl"
    if hawk_dove_axis_path is None:
        hawk_dove_axis_path = Path(__file__).parent.parent.parent / "data" / "hawk_dove_axis.pkl"

    # Convert to Path objects
    csv_path = Path(csv_path)
    output_pkl_path = Path(output_pkl_path)
    hawk_dove_axis_path = Path(hawk_dove_axis_path)

    try:
        # Check if files exist
        if not csv_path.exists():
            return False, f"CSV file not found: {csv_path}"
        if not hawk_dove_axis_path.exists():
            return False, f"Hawk-dove axis not found: {hawk_dove_axis_path}"

        # Load CSV data
        df = pd.read_csv(csv_path)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Load embedding model
        model = SentenceTransformer("all-mpnet-base-v2")
        embeddings = model.encode(df['text'].tolist(), show_progress_bar=False)

        # Load hawk-dove axis
        with open(hawk_dove_axis_path, 'rb') as f:
            hawk_dove_axis = pickle.load(f)

        # Calculate hawk-dove scores
        hawk_dove_scores = embeddings @ hawk_dove_axis

        # Calculate drift (cosine distance from previous meeting)
        drifts = [0.0]  # First meeting has no drift
        for i in range(1, len(embeddings)):
            sim = cosine_similarity([embeddings[i-1]], [embeddings[i]])[0][0]
            drifts.append(1 - sim)

        # Calculate EWM z-scores
        scores_series = pd.Series(hawk_dove_scores)
        ewm = scores_series.ewm(span=15).mean()
        ewm_std = scores_series.ewm(span=15).std()
        hawk_dove_zscores = (hawk_dove_scores - ewm) / ewm_std

        # Create updated DataFrame
        df['hawk_dove_score'] = hawk_dove_scores
        df['hawk_dove_zscore'] = hawk_dove_zscores
        df['drifts'] = drifts  # Use 'drifts' to match existing data
        df['embedding'] = [emb.tolist() for emb in embeddings]

        # Save to pickle
        output_pkl_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_pickle(output_pkl_path)

        num_statements = len(df)
        latest_date = df['date'].max().strftime('%Y-%m-%d')

        return True, f"Reprocessed {num_statements} statements. Latest: {latest_date}"

    except Exception as e:
        return False, f"Error reprocessing data: {str(e)}"


def get_last_update_time(pkl_path: str | None = None) -> str:
    """Get the last modification time of the data file

    Args:
        pkl_path: Path to the pickle file (defaults to data/fomc_data.pkl)

    Returns:
        Formatted timestamp string
    """
    if pkl_path is None:
        pkl_path = Path(__file__).parent.parent.parent / "data" / "fomc_data.pkl"

    try:
        path = Path(pkl_path)
        if path.exists():
            mtime = path.stat().st_mtime
            dt = datetime.fromtimestamp(mtime)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "Never"
    except Exception:
        return "Unknown"
