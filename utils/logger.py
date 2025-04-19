import pandas as pd
from datetime import datetime
import os

def log_entry(
    required_habits: dict,
    bonus_habits: dict,
    mood: str,
    reflection: str,
    sentiment_score: float,
    alignment_score: float,
    recommendations: list[str],
    log_file: str = "data/logs.csv"
):
    """
    Appends a new entry to the CSV log file.
    """
    # Combine everything into one flat dictionary
    entry = {
        "timestamp": datetime.now().isoformat(),
        "mood": mood,
        "sentiment_score": sentiment_score,
        "alignment_score": alignment_score,
        "reflection": reflection,
        "recommendations": "; ".join(recommendations),
    }

    # Add habits (e.g., Pray Fajr: True)
    entry.update(required_habits)
    entry.update(bonus_habits)

    # Create DataFrame
    df = pd.DataFrame([entry])

    # Append or create the file
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    if os.path.exists(log_file):
        df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        df.to_csv(log_file, mode="w", header=True, index=False)
