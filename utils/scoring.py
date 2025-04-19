def calculate_alignment_score(
    required_habits: dict,
    bonus_habits: dict,
    mood: str,
    sentiment_score: float
) -> float:
    """
    Calculates an alignment score between 0.0 and 1.0 based on:
    - Habits completed
    - Mood emoji
    - Sentiment score of reflection
    """
    # Required habits: more important
    required_score = sum(required_habits.values()) / len(required_habits)

    # Bonus habits: supportive but optional
    bonus_score = sum(bonus_habits.values()) / len(bonus_habits)

    # Mood: Map emoji to mood score
    mood_scores = {
        "😊": 1.0,
        "😐": 0.5,
        "😤": 0.25,
        "😭": 0.0,
        "🧘": 0.9
    }
    mood_score = mood_scores.get(mood, 0.5)

    # Sentiment is already -1.0 to +1.0 → rescale to 0 to 1
    normalized_sentiment = (sentiment_score + 1) / 2

    # Weighted average of all components
    alignment = (
        (required_score * 0.4) +
        (bonus_score * 0.2) +
        (mood_score * 0.2) +
        (normalized_sentiment * 0.2)
    )

    return round(alignment, 3)
