import streamlit as st
import pandas as pd
from datetime import date
import os


# Import utils
try:
    from utils.sentiment import analyze_sentiment
    from utils.scoring import calculate_alignment_score
    from utils.recommender import suggest_habits
    from utils.logger import log_entry
except ImportError as e:
    st.error(f"Error importing utility functions: {e}")
    st.stop()

# --- Define Habits ---
# Outside the main logic so they are consistent
REQUIRED_HABITS_LIST = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Read Qur'an", "No Caffeine"]
BONUS_HABITS_LIST = ["Stretch", "Journal", "Lowered Gaze"]
MOOD_OPTIONS = ["😊", "😐", "😤", "😭", "🧘"]

# --- Session State Initialization ---
today = date.today()

# Initialize state if keys don't exist or if the date changed
if 'app_date' not in st.session_state or st.session_state.app_date != today:
    st.session_state.app_date = today # Store today's date
    st.session_state.required_completion = {habit: False for habit in REQUIRED_HABITS_LIST}
    st.session_state.bonus_completion = {habit: False for habit in BONUS_HABITS_LIST}
    st.session_state.mood = MOOD_OPTIONS[1] # Default to neutral '😐'
    st.session_state.reflection = ""
    st.session_state.dua = ""
    st.session_state.saved_today = False # Track if saved for today
    st.session_state.sentiment_score = 0.0 # Initial placeholders
    st.session_state.alignment_score = 0.0
    st.session_state.recommendations = []
    print(f"Session state initialized/reset for {today}") # Debug print



# --- Main App UI ---
st.set_page_config(page_title="Tazkiyah", layout="centered")
st.title("🕊️ Tazkiyah – Daily Check-in")
st.write(f"Entries for: {st.session_state.app_date.strftime('%B %d, %Y')}") # Display current date



# --- Habits ---
st.header("✅ Daily Habits")
# Create checkboxes dynamically, binding to session state
for i, habit in enumerate(REQUIRED_HABITS_LIST):
    st.session_state.required_completion[habit] = st.checkbox(
        habit,
        key=f"required_{habit}", # Unique key using habit name
        value=st.session_state.required_completion[habit] # Use state value
    )

st.subheader("⭐ Bonus Habits")
for i, habit in enumerate(BONUS_HABITS_LIST):
    st.session_state.bonus_completion[habit] = st.checkbox(
        habit,
        key=f"bonus_{habit}", # Unique key using habit name
        value=st.session_state.bonus_completion[habit] # Use state value
    )

# --- Mood ---
st.header("🌦️ Mood")
st.session_state.mood = st.radio(
    "How are you feeling today?",
    options=MOOD_OPTIONS,
    key="mood_radio", # Unique key
    index=MOOD_OPTIONS.index(st.session_state.mood) # Set index based on state
)


# --- Reflection ---
st.header("✍️ Reflection")
st.session_state.reflection = st.text_area(
    "Write anything on your mind today:",
    key="reflection_input", # Unique key
    value=st.session_state.reflection # Use state value
)

# --- Du'a ---
st.header("🤲 Du'a / Intention")
st.session_state.dua = st.text_area(
    "Any du’a or personal intention today? (Optional)",
    key="dua_input", # Unique key
    value=st.session_state.dua # Use state value
)


# --- Dynamic Calculation & Feedback (Runs on every interaction) ---
# Perform calculations using current session state values
try:
    st.session_state.sentiment_score = analyze_sentiment(st.session_state.reflection)

    st.session_state.alignment_score = calculate_alignment_score(
        st.session_state.required_completion, # Pass the dict from state
        st.session_state.bonus_completion,   # Pass the dict from state
        st.session_state.mood,               # Pass mood from state
        st.session_state.sentiment_score     # Pass current sentiment
    )

    st.session_state.recommendations = suggest_habits(
        st.session_state.required_completion,
        st.session_state.bonus_completion,
        st.session_state.mood,
        st.session_state.alignment_score
    )
except Exception as e:
    st.error(f"Error during feedback calculation: {e}")
    # Reset calculated values in state if error occurs
    st.session_state.sentiment_score = 0.0
    st.session_state.alignment_score = 0.0
    st.session_state.recommendations = []

st.markdown("---")
st.header("📈 Instant Feedback")

# Display Sentiment
st.markdown("### 🧠 Sentiment Analysis")
_sentiment_score = st.session_state.sentiment_score # Use temporary variable for display checks
if _sentiment_score > 0.2:
    st.info(f"Reflection seems **positive**. (Score: {_sentiment_score})")
elif _sentiment_score < -0.2:
    st.warning(f"Reflection seems **negative**. (Score: {_sentiment_score})")
else:
    st.write(f"Reflection seems **neutral**. (Score: {_sentiment_score})")

# Display Alignment
st.markdown("### 🧭 Alignment Score")
_alignment_score = st.session_state.alignment_score # Use temporary variable for display checks
if _alignment_score > 0.75:
    st.success(f"Highly aligned today! (Score: {_alignment_score})")
elif _alignment_score > 0.4:
    st.info(f"Moderately aligned. (Score: {_alignment_score})")
else:
    st.warning(f"Potentially out of sync. (Score: {_alignment_score})")

# Display Recommendations
st.markdown("### 🔁 Suggested Habits for Tomorrow")
_recommendations = st.session_state.recommendations # Use temporary variable for display checks
if _recommendations:
    for habit in _recommendations:
        st.markdown(f"- {habit}")
else:
    st.write("Keep up the great work! 🙌")


# --- Save Button & Logic ---
st.markdown("---")

if st.button("💾 Save Final Entry for Today", key="save_button"):

    # 1. Check if already saved today using session state flag
    if st.session_state.saved_today:
        st.info("✅ Today's entry has already been saved.")
    else:
        # 2. Log the current state
        log_path = "data/logs.csv" # Define log path here or get from config
        try:
            log_entry(
                required_habits=st.session_state.required_completion,
                bonus_habits=st.session_state.bonus_completion,
                mood=st.session_state.mood,
                reflection=st.session_state.reflection,
                # Use the already calculated values from session state
                sentiment_score=st.session_state.sentiment_score,
                alignment_score=st.session_state.alignment_score,
                recommendations=st.session_state.recommendations,
                log_file=log_path
            )
            st.success("💾 Entry for today saved successfully!")
            # 3. Set the flag in session state to prevent re-saving
            st.session_state.saved_today = True
        except Exception as e:
            st.error(f"Error saving log entry: {e}")

# Optional: Display save status persistently
if st.session_state.saved_today:
     st.sidebar.success(f"Log saved for {st.session_state.app_date.strftime('%Y-%m-%d')}")