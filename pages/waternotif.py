import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from plyer import notification

# Initialize session state (using native Streamlit function)
if 'consumed_ml' not in st.session_state:
    st.session_state.consumed_ml = 0
if 'daily_goal_ml' not in st.session_state:
    st.session_state.daily_goal_ml = {}
if 'current_day' not in st.session_state:
    st.session_state.current_day = None
if 'history' not in st.session_state:
    st.session_state.history = {}  # Dictionary to store daily water intake

# Initialize a variable to track the last time the "Drink 500 ml" button was clicked
last_drink_time = 0

# Initialize a flag to control the notification
notification_flag = True

# Define a list of colors for the graphs
line_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Define an offset for target lines when goals are the same
target_line_offset = 10


def send_notification():
    current_time = time.time()
    if current_time - last_drink_time > 2 and notification_flag:
        notification_title = "Water Reminder"
        notification_message = f"Have you had 500 ml of water?"
        notification_timeout = 10  # Adjust the timeout as needed

        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=notification_timeout,
        )


def main():
    st.title("Water Tracker")

    # Dropdown to select the day of the week
    selected_day = st.selectbox("Select Day of the Week",
                                ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    # Check if the selected day is a new day; if so, reset the progress and goal
    if st.session_state.current_day != selected_day:
        st.session_state.current_day = selected_day
        st.session_state.daily_goal_ml[selected_day] = 0
        st.session_state.consumed_ml = 0
        notification_flag = True  # Reset the notification flag

    # Input field to set the daily goal (incremented by 500ml on each button click)
    st.write(f"Daily Goal for {selected_day}:")
    st.session_state.daily_goal_ml[selected_day] = st.number_input("Set Goal (500ml increments):",
                                                                   value=st.session_state.daily_goal_ml.get(
                                                                       selected_day, 0), step=500)

    # Button to increment water consumption and trigger the notification
    if st.button("Drink 500 ml"):
        st.session_state.consumed_ml += 500
        last_drink_time = time.time()
        if st.session_state.consumed_ml >= st.session_state.daily_goal_ml[selected_day]:
            notification_flag = False  # Stop the notification if the goal is reached
        send_notification()

    # Button to mark "Done for the Day"
    if st.button("Done for the Day"):
        notification_flag = True  # Reset the notification flag
        st.session_state.history[selected_day] = st.session_state.consumed_ml

        # Check if the user reached the daily goal, and display the graph and congrats message
        if st.session_state.consumed_ml >= st.session_state.daily_goal_ml[selected_day]:
            st.text(
                f"Congratulations! You reached your goal of {st.session_state.daily_goal_ml[selected_day]} ml for {selected_day}.")
            st.session_state.consumed_ml = 0  # Reset consumed_ml if goal is reached

    # Calculate the progress and display a progress bar
    if st.session_state.daily_goal_ml[selected_day] != 0:
        progress = (st.session_state.consumed_ml / st.session_state.daily_goal_ml[selected_day]) * 100
    else:
        progress = 0

    st.write(f"Progress for {selected_day}: {progress:.1f}%")
    st.progress(progress / 100)

    # Display water intake history as bar graphs for all days
    if st.session_state.history:
        st.write("Water Intake History:")
        data = pd.DataFrame(list(st.session_state.history.items()), columns=['Day', 'Intake (ml)'])
        fig, ax = plt.subplots()

        # Initialize a dictionary to store the vertical position of target lines for each day
        target_lines = {}

        # Plot each day's water intake graph with a different color and add corresponding target line
        for day, intake in st.session_state.history.items():
            color = line_colors[list(st.session_state.history.keys()).index(day)]
            ax.bar(day, intake, color=color, label=day)
            goal = st.session_state.daily_goal_ml[day]

            # Check if there is already a target line for the same goal
            if goal in target_lines:
                # Increment the vertical position by the offset
                target_lines[goal] += target_line_offset
            else:
                target_lines[goal] = target_line_offset

            # Calculate the vertical position for the target line
            target_line_position = goal + target_lines[goal]

            ax.axhline(y= target_line_position, color=color, linestyle='--', label=f'{day} Goal')

        ax.legend()
        st.pyplot(fig)

    # Button to clear the history and reset the progress
    if st.button("Clear History"):
        st.session_state.history = {}
        st.session_state.consumed_ml = 0
        st.session_state.daily_goal_ml = {}


if __name__ == "__main__":
    main()