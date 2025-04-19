import streamlit as st
from utils.sentiment import analyze_sentiment
from utils.scoring import calculate_alignment_score
from utils.recommender import suggest_habits
from utils.logger import log_entry


st.set_page_config(page_title="Tazkiyah", layout="centered")

st.title("🕊️ Tazkiyah – Daily Habit & Reflection Tracker")

# --- Habits ---
st.header("✅ Daily Habits")
required_habits = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Read Qur'an", "No Caffeine"]
bonus_habits = ["Stretch", "Journal", "Lowered Gaze"]

completed_required = {
    habit: st.checkbox(habit, key=f"required_{i}")
    for i, habit in enumerate(required_habits)
}

completed_bonus = {
    habit: st.checkbox(habit, key=f"bonus_{i}")
    for i, habit in enumerate(bonus_habits)
}

# --- Mood ---
st.header("🌦️ Mood")
mood = st.radio("How are you feeling today?", ["😊", "😐", "😤", "😭", "🧘"])

# --- Reflection ---
st.header("✍️ Reflection")
reflection = st.text_area("Write anything on your mind today:")

# --- Du'a ---
dua = st.text_area("🤲 Any du’a or personal intention today? (Optional)")

# --- Submission ---
if st.button("Submit Entry"):
    st.success("Submitted!")

    # --- Sentiment Analysis ---
    sentiment_score = analyze_sentiment(reflection)

    st.markdown("### 🧠 Sentiment Analysis")
    if sentiment_score > 0.2:
        st.info(f"Your reflection seems **positive**. (Score: {sentiment_score})")
    elif sentiment_score < -0.2:
        st.warning(f"Your reflection seems **negative**. (Score: {sentiment_score})")
    else:
        st.write(f"Your reflection seems **neutral**. (Score: {sentiment_score})")

    # --- Alignment Scoring ---
    alignment_score = calculate_alignment_score(
        completed_required,
        completed_bonus,
        mood,
        sentiment_score
    )

    st.markdown("### 🧭 Alignment Score")
    if alignment_score > 0.75:
        st.success(f"You're highly aligned today. (Score: {alignment_score})")
    elif alignment_score > 0.4:
        st.info(f"You're moderately aligned. Keep going. (Score: {alignment_score})")
    else:
        st.warning(f"You may be out of sync. Consider a reset. (Score: {alignment_score})")

    # --- Habit Recommendations ---
    recommendations = suggest_habits(
        completed_required,
        completed_bonus,
        mood,
        alignment_score
    )

    st.markdown("### 🔁 Suggested Habits for Tomorrow")
    if recommendations:
        for habit in recommendations:
            st.markdown(f"- {habit}")
    else:
        st.write("You're doing great! No suggestions for tomorrow 🙌")


    log_entry(
    completed_required,
    completed_bonus,
    mood,
    reflection,
    sentiment_score,
    alignment_score,
    recommendations
    )




