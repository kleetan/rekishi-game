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

    # Score tracking
    if "score" not in st.session_state:
        st.session_state.score = 0

    st.markdown(f"**Score:** {st.session_state.score}")

    if st.button("Reset Score"):
        st.session_state.score = 0

    # Era filter
    era_filter = st.radio(
        "Select era",
        ["All", "BC only", "AD only"],
        horizontal=True
    )

    # Filter by era
    if era_filter == "BC only":
        df = df[df['year'] < 0]
    elif era_filter == "AD only":
        df = df[df['year'] >= 0]

    # If no data after filtering
    if df.empty:
        st.error("No events available for the selected era.")
        st.stop()

    # Year range slider
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.slider(
        "Select year range for questions",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Number of choices
    num_choices = st.selectbox("Select number of events (up to 10)", options=list(range(2, 11)), index=4)

    # Start button to begin game
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    if st.button("Start Game"):
        st.session_state.game_started = True
        st.session_state.start_time = time.time()
        st.session_state.new_problem = True

    if not st.session_state.game_started:
        st.stop()

    # Filter by range
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    events = dict(zip(filtered_df['event'], filtered_df['year']))

    # Check if enough events
    if len(events) < num_choices:
        st.error(f"Only {len(events)} events available in this range. Please choose fewer.")
        st.stop()

    # Track problem state
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

    # Generate sample events
    if "sample_events" not in st.session_state or st.session_state.new_problem:
        st.session_state.sample_events = random.sample(list(events.items()), num_choices)
        st.session_state.new_problem = False
        st.session_state.start_time = time.time()

    sample_events = st.session_state.sample_events
    event_names = [e[0] for e in sample_events]

    # Show elapsed time
    elapsed_time = int(time.time() - st.session_state.start_time)
    st.markdown(f"**⏱ Elapsed Time:** {elapsed_time} seconds")

    # Sortable UI
    sorted_events = sort_items(event_names, direction="vertical")

    # Check correctness
    if st.button("Check if correct"):
        correct_order = sorted(sample_events, key=lambda x: x[1])
        correct_names = [e[0] for e in correct_order]

        if sorted_events == correct_names:
            bonus = max(10 - elapsed_time, 0)  # time bonus
            points = 10 + bonus
            st.session_state.score += points
            st.success(f"🎉 Correct! +{points} points")
        else:
            st.error("❌ Incorrect.")

    # Show number of correct positions
    if st.button("Check number of correct positions"):
        correct_order = sorted(sample_events, key=lambda x: x[1])
        correct_names = [e[0] for e in correct_order]

        correct_count = sum([1 for user, correct in zip(sorted_events, correct_names) if user == correct])
        st.info(f"✅ You have {correct_count} events in the correct position.")

    # Show correct answer
    if st.button("Show correct order"):
        correct_order = sorted(sample_events, key=lambda x: x[1])
        st.write("The correct order is:")
        for i, (event, year) in enumerate(correct_order, 1):
            st.write(f"{i}. {event} ({year})")

    # New problem
    if st.button("Generate new problem"):
        st.session_state.new_problem = True
        st.session_state.start_time = time.time()
