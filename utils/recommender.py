def suggest_habits(
    required_habits: dict,
    bonus_habits: dict,
    mood: str,
    alignment_score: float
) -> list[str]:
    """
    Recommends habits to focus on tomorrow based on missed ones,
    current mood, and alignment score.
    """
    suggestions = []

    # --- Prioritize missed required habits
    for habit, completed in required_habits.items():
        if not completed:
            suggestions.append(habit)

    # --- If user is low alignment or negative mood, boost self-care habits
    if alignment_score < 0.5 or mood in ["😭", "😤"]:
        emotional_boosters = ["Stretch", "Journal", "Lowered Gaze"]
        for habit in emotional_boosters:
            if habit in bonus_habits and not bonus_habits[habit]:
                suggestions.append(habit)

    # --- Remove duplicates and limit to 3
    unique = list(dict.fromkeys(suggestions))
    return unique[:3]
