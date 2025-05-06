import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import random
import time

# Load CSV (Only once)
if 'df' not in st.session_state:
    df = pd.read_csv('nenpyou.csv')
    df = df.dropna(subset=['event', 'year'])
    df['year'] = df['year'].astype(int)
    st.session_state.df = df  # Store in session state to prevent reloading every time

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

    # Initialize session state
    if "screen" not in st.session_state:
        st.session_state.screen = "start"
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0.0
    if "score" not in st.session_state:
        st.session_state.score = 0.0
    if "used_check_positions" not in st.session_state:
        st.session_state.used_check_positions = False
    if "new_problem" not in st.session_state:
        st.session_state.new_problem = True
    if "total_score" not in st.session_state:
        st.session_state.total_score = 0.0
    if "games_played" not in st.session_state:
        st.session_state.games_played = 0

    if st.session_state.screen == "start":
        # Select era, range, and number of events before starting
        era_filter = st.radio("Select era", ["All", "BC only", "AD only"], horizontal=True)
        min_year = int(st.session_state.df['year'].min())
        max_year = int(st.session_state.df['year'].max())
        year_range = st.slider("Select year range", min_year, max_year, (min_year, max_year))
        num_choices = st.selectbox("Select number of events (up to 10)", options=list(range(2, 11)), index=4)

        # Start the game button
        if st.button("Start Game"):
            st.session_state.screen = "game"
            st.session_state.era_filter = era_filter
            st.session_state.year_range = year_range
            st.session_state.num_choices = num_choices
            st.session_state.start_time = time.time()  # Start the timer when the game starts
            st.session_state.new_problem = True
            st.session_state.used_check_positions = False
            st.session_state.score = 0.0  # Reset score when starting new game
            st.session_state.force_rerun = False  # Remove the force rerun flag
            st.session_state.games_played += 1  # Increment the number of games played

        st.stop()

    # If it's the "game" screen, proceed with the game logic
    if st.session_state.screen == "game":
        # Filter data based on selected era
        df = st.session_state.df  # Use session state df instead of reloading
        if st.session_state.era_filter == "BC only":
            df = df[df['year'] < 0]
        elif st.session_state.era_filter == "AD only":
            df = df[df['year'] >= 0]

        # If no data after filtering
        if df.empty:
            st.error("No events available for the selected era.")
            st.stop()

        # Filter by selected year range
        filtered_df = df[(df['year'] >= st.session_state.year_range[0]) & (df['year'] <= st.session_state.year_range[1])]
        events = dict(zip(filtered_df['event'], filtered_df['year']))

        # If not enough events are available
        if len(events) < st.session_state.num_choices:
            st.error(f"Only {len(events)} events available. Please choose fewer.")
            st.stop()

        # Reset problem if needed
        if "last_num" not in st.session_state or st.session_state.last_num != st.session_state.num_choices or "last_range" not in st.session_state or st.session_state.last_range != st.session_state.year_range or "last_era" not in st.session_state or st.session_state.last_era != st.session_state.era_filter:
            st.session_state.new_problem = True
            st.session_state.last_num = st.session_state.num_choices
            st.session_state.last_range = st.session_state.year_range
            st.session_state.last_era = st.session_state.era_filter

        # Generate sample events
        if st.session_state.new_problem:
            st.session_state.sample_events = random.sample(list(events.items()), st.session_state.num_choices)
            st.session_state.new_problem = False
            st.session_state.used_check_positions = False

        sample_events = st.session_state.sample_events
        event_names = [e[0] for e in sample_events]

        # Sortable UI
        sorted_events = sort_items(event_names, direction="vertical")

        # Timer
        elapsed_time = time.time() - st.session_state.start_time  # No longer displayed

        # Check correctness
        if st.button("Check if correct"):
            correct_order = sorted(sample_events, key=lambda x: x[1])
            correct_names = [e[0] for e in correct_order]

            if sorted_events == correct_names:
                st.success("🎉 Correct!")
                gained_score = 100 / elapsed_time
                if st.session_state.used_check_positions:
                    gained_score /= 2
                    st.info("Score halved because 'Check number of correct positions' was used.")
                st.session_state.score += gained_score
                st.session_state.total_score += gained_score
                st.success(f"🏆 Score: {st.session_state.score:.2f}")
            else:
                st.error("❌ Incorrect.")

        # Show number of correct positions
        if st.button("Check number of correct positions"):
            correct_order = sorted(sample_events, key=lambda x: x[1])
            correct_names = [e[0] for e in correct_order]
            correct_count = sum([1 for user, correct in zip(sorted_events, correct_names) if user == correct])
            st.info(f"✅ You have {correct_count} events in the correct position.")
            st.session_state.used_check_positions = True

        # Show correct answer
        if st.button("Show correct order"):
            correct_order = sorted(sample_events, key=lambda x: x[1])
            st.write("The correct order is:")
            for i, (event, year) in enumerate(correct_order, 1):
                st.write(f"{i}. {event} ({year})")

        # New problem
        if st.button("Generate new problem"):
            st.session_state.new_problem = True
            st.session_state.start_time = time.time()  # Reset the timer when new problem is generated
            st.experimental_rerun()  # Force the rerun to immediately show the new problem

        # End game and show average score
        if st.button("End Game"):
            if st.session_state.games_played > 0:
                average_score = st.session_state.total_score / st.session_state.games_played
                st.write(f"🏅 Average Score: {average_score:.2f}")
            st.session_state.screen = "start"  # Go back to the start screen
            st.session_state.total_score = 0.0  # Reset total score after game ends
            st.session_state.games_played = 0  # Reset games played
            st.experimental_rerun()  # Restart the app to reset all states
