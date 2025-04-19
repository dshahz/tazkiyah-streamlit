from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """
    Returns a sentiment polarity score between -1.0 (very negative) and +1.0 (very positive)
    """
    if not text.strip():
        return 0.0  # Treat empty reflections as neutral
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 3)