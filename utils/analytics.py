import pandas as pd

def calculate_streak(data: pd.DataFrame, habit_column: str) -> int:
    if data.empty:
        return 0
    
    if habit_column not in data.columns:
        print(f"Error: '{habit_column}' not found in DataFrame for streak calclation ")
        return 0
    
    habit_series = data[habit_column]
    filled_series = habit_series.fillna(0)
    boolean_series = filled_series.astype(bool)
    bool_series_reversed = boolean_series[::-1]
    streak = 0
    for item in bool_series_reversed:
        if item == True:
            streak += 1
        else:
            break
    
    return streak