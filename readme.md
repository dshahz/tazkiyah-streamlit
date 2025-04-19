# Tazkiyah: Daily Alignment & Reflection App

> Track habits, mood, and reflections to cultivate intentional living.

---

## 📖 Overview

**Tazkiyah** means purification and growth. This Streamlit application provides a personal dashboard for daily self-reflection and habit tracking, designed to help users live more intentionally and align their actions with their values.

It offers a simple interface to log daily habits (spiritual, physical, mental), track mood, journal reflections, and receive immediate feedback on sentiment and personal alignment. A dedicated progress dashboard helps visualize trends over time.

While inspired by Islamic principles of self-development, the app is designed to be universally applicable for anyone seeking greater self-awareness, discipline, and mindful growth.

---

## Features

**Daily Check-in (`app.py`):**
*   Track completion of customizable **required habits** (e.g., 5 daily prayers, reading, no caffeine).
*    Track completion of customizable **bonus habits** (e.g., stretching, journaling, lowering gaze).
*    Log daily **mood** using intuitive emojis.
*    Write free-form **reflections** on the day.
*    Optionally record private **du'as** or intentions.
*    Receive instant **sentiment analysis** score for reflections (using TextBlob).
*    Get a calculated **alignment score** based on habits, mood, and sentiment.
*    Receive **habit recommendations** for the next day based on current input.
*    Automatically **logs** each entry to `data/logs.csv` (if not excluded by `.gitignore`).

**Progress Dashboard (`pages/📊 Progress Dashboard.py`):**
*    Visualize **alignment score** trends over time.
*    View **mood frequency** distribution.
*    Track **required habit consistency** with completion counts.

---

##  Technologies Used

*   **Framework:** Streamlit
*   **Language:** Python 3.11
*   **Data Handling:** Pandas
*   **NLP (Sentiment):** TextBlob
*   **Plotting:** Streamlit's native charts (based on Vega-Lite/Matplotlib)

---

##  How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/dshahz/tazkiyah-streamlit.git
    cd tazkiyah-streamlit 
    ```
2.  **Install Dependencies:**
    *   (Recommended) Create and activate a virtual environment.
    *   Install the required packages:
        ```bash
        pip install streamlit pandas textblob
        ```
    *   Download TextBlob corpora (needed for sentiment analysis):
        ```bash
        python -m textblob.download_corpora
        ```
    *(Note: You might want to create a `requirements.txt` file later for easier dependency management: `pip freeze > requirements.txt`)*

3.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
4.  **View the App:** Open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

---

##  Project Structure