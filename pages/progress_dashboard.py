import streamlit as st
import pandas as pd
import os
from utils.analytics import calculate_streak

st.set_page_config(page_title="Progress Dashboard", layout="centered")
st.title("📊 Your Progress Dashboard")

# Load the log data
log_path = "data/logs.csv"

if not os.path.exists(log_path):
    st.warning("No logs found yet. Start by completing a check-in on the main page.")
else:
    df = pd.read_csv(log_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by='timestamp') # Reassign the sorted result back to df

# --- Calculate Streaks ---
# Define the prayer columns
prayer_columns = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"] 
streak_results = {} # Use a dictionary to store results

for prayer in prayer_columns:
    # Check if column exists before calculating streak
    if prayer in df.columns:
        streak_results[prayer] = calculate_streak(df, prayer)
    else:
        streak_results[prayer] = 0 # Or None, or handle appropriately
        




# --- Display Streaks ---
st.subheader("☀️ Prayer Streaks")
cols = st.columns(len(prayer_columns)) # Create 5 columns

for i, prayer in enumerate(prayer_columns):
    with cols[i]:
        st.metric(label=prayer, value=f"{streak_results.get(prayer, 0)} days") 
        # streak_results.get(prayer, 0) safely gets the value or defaults to 0

st.markdown("---") # Add a divider before other charts

# ... (Your existing charts for Alignment, Mood, Consistency) ...



# --- Alignment Over Time ---
st.subheader("🧭 Alignment Over Time")
st.line_chart(df.set_index("timestamp")["alignment_score"])

# --- Mood Frequency ---
st.subheader("😊 Mood Trends")
mood_counts = df["mood"].value_counts()
st.bar_chart(mood_counts)

# --- Required Habit Completion ---
st.subheader("✅ Required Habit Consistency")
required = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Read Qur'an", "No Caffeine"]
    

existing_required_cols = [col for col in required if col in df.columns] 

if not existing_required_cols:
    st.info("No data found for required habits.") # Changed message slightly
else:
    # Calculate sums only for existing columns
    completed_totals = df[existing_required_cols].sum()
    st.bar_chart(completed_totals)

    
