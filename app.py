import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import random
import time

# Load CSV
df = pd.read_csv('nenpyou.csv')

# Clean data
df = df.dropna(subset=['event', 'year'])
df['year'] = df['year'].astype(int)

# Layout: left image, center content, right image
left_col, center_col, right_col = st.columns([1, 15, 1])

with left_col:
    st.image("britain.png", use_container_width=True)

with right_col:
    st.image("soviet.png", use_container_width=True)

with center_col:
    st.title("📜 Timeline Sorting Game")
    st.write("Sort the historical events below in **chronological order**.")
    st.caption("Unless otherwise specified, refers to the time of commencement.")

    # Score initialization
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 0

    st.markdown(f"### Score: {st.session_state.score} / {st.session_state.total_questions}")

    # Timer setup
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # Era filter
    era_filter = st.radio("Select era", ["All", "BC only", "AD only"], horizontal=True)
    if era_filter == "BC only":
        df = df[df['year'] < 0]
    elif era_filter == "AD only":
        df = df[df['year'] >= 0]

    if df.empty:
        st.error("No events available for the selected era.")
        st.stop()

    # Year range slider
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.slider("Select year range for questions", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    events = dict(zip(filtered_df['event'], filtered_df['year']))

    num_choices = st.selectbox("Select number of events (up to 10)", options=list(range(2, 11)), index=4)

    if len(events) < num_choices:
        st.error(f"Only {len(events)} events available in this range. Please choose fewer.")
        st.stop()

    if "new_problem" not in st.session_state:
        st.session_state.new_problem = True

    if (
        "last_num" not in st.session_state or
        st.session_state.last_num != num_choices or
        "last_range" not in st.session_state or
        st.session_state.last_range != year_range or
        "last_era" not in st.session_state or
        st.session_state.last_era != era_filter
    ):
        st.session_state.new_problem = True
        st.session_state.last_num = num_choices
        st.session_state.last_range = year_range
        st.session_state.last_era = era_filter

    if "sample_events" not in st.session_state or st.session_state.new_problem:
        st.session_state.sample_events = random.sample(list(events.items()), num_choices)
        st.session_state.start_time = time.time()
        st.session_state.new_problem = False

    sample_events = st.session_state.sample_events
    event_names = [e[0] for e in sample_events]

    sorted_events = sort_items(event_names, direction="vertical")

    if st.button("Check if correct"):
        elapsed_time = round(time.time() - st.session_state.start_time, 2)
        correct_order = sorted(sample_events, key=lambda x: x[1])
        correct_names = [e[0] for e in correct_order]

        st.session_state.total_questions += 1

        if sorted_events == correct_names:
            time_bonus = max(0, 10 - int(elapsed_time))  # Faster = higher score bonus
            score_gain = 10 + time_bonus
            st.session_state.score += score_gain
            st.success(f"🎉 Correct! (+{score_gain} points, answered in {elapsed_time} seconds)")
        else:
            st.warning(f"❌ Incorrect. (answered in {elapsed_time} seconds)")

    if st.button("Check number of correct positions"):
        correct_order = sorted(sample_events, key=lambda x: x[1])
        correct_names = [e[0] for e in correct_order]
        correct_count = sum([1 for user, correct in zip(sorted_events, correct_names) if user == correct])
        st.info(f"✅ You have {correct_count} events in the correct position.")

    if st.button("Show correct order"):
        correct_order = sorted(sample_events, key=lambda x: x[1])
        st.write("The correct order is:")
        for i, (event, year) in enumerate(correct_order, 1):
            st.write(f"{i}. {event} ({year})")

    if st.button("Generate new problem"):
        st.session_state.new_problem = True

    if st.button("Reset Score"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
