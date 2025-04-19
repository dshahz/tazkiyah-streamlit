import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Progress Dashboard", layout="centered")
st.title("📊 Your Progress Dashboard")

# Load the log data
log_path = "data/logs.csv"

if not os.path.exists(log_path):
    st.warning("No logs found yet. Start by completing a check-in on the main page.")
else:
    df = pd.read_csv(log_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Alignment Over Time ---
    st.subheader("🧭 Alignment Over Time")
    st.line_chart(df.set_index("timestamp")["alignment_score"])

    # --- Mood Frequency ---
    st.subheader("😊 Mood Trends")
    mood_counts = df["mood"].value_counts()
    st.bar_chart(mood_counts)

    # --- Required Habit Completion ---
    st.subheader("✅ Required Habit Consistency")
    required = ["Pray Fajr", "Read Qur'an", "No Caffeine"]
    completed_totals = df[required].sum()
    st.bar_chart(completed_totals)
