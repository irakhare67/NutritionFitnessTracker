import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import requests
import pandas as pd
import os
import streamlit as st
import cv2
import os
import time
import csv
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import os
names = ["Aniket","pranav","karan"]
usernames=["aniket","pranav","karan"]
file_path=os.path.join(os.path.dirname(__file__), "hashed_pw.pkl")
with open(file_path, "rb") as file:
    hashed_passwords=pickle.load(file)
authenticator=stauth.Authenticate(names,usernames,hashed_passwords,"student_dashboard","abcdef",cookie_expiry_days=30) 
name,authentication_status,username=authenticator.login("Login","main")
if authentication_status==False:
    st.error("Username/Password is incorrect")
if authentication_status==None:
    st.warning("Please enter your username and password")
if authentication_status:

        # Set up the API endpoint and headers
        url = "https://api.api-ninjas.com/v1/nutrition?query="
        headers = {
            "X-API-Key": "cSNXvt31N7FSRia1HJfJlg==j3XuZh8S3Cw6Aqwg"
        }

        # Create a background image
        st.markdown(
            """
            <style>
            .stApp {
                background-image: url('https://img.freepik.com/premium-photo/healthy-food-variation-with-copy-space-empty-background_944892-519.jpg');
                background-size: cover;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Create a title and header
        st.title(f"Nutrition Information {name}")

        # Check if the search history CSV file exists, and create it if not
        search_history_file = "search_history.csv"
        if not os.path.exists(search_history_file):
            pd.DataFrame(columns=["Food", "Calories"]).to_csv(search_history_file, index=False)

        # Create the input field and submit button
        food_item = st.text_input("Enter a food item")
        if st.button("Submit"):
            # Make the API request
            params = {"query": food_item}
            response = requests.get(url, headers=headers, params=params)

            # Parse the response and display the calorie information
            if response.status_code == 200:
                result = response.json()
                if len(result) > 0:
                    # Assuming you want to display the first result's calories
                    calories = result[0]["calories"]
                    st.success(f"{food_item} has {calories} calories")

                    # Update the search history by appending to the CSV file
                    search_history = pd.read_csv(search_history_file)
                    search_history = search_history.append({"Food": food_item, "Calories": calories}, ignore_index=True)
                    search_history.to_csv(search_history_file, index=False)

                else:
                    st.warning("No results found for this food item")
            else:
                st.error("Error: Unable to get calorie information")

        # Create a section for history
        st.header("Search History")
        authenticator.logout("Logout","sidebar")

        # Load and display the search history from the CSV file when the "Show History" button is pressed
        if st.button("Show History"):
            search_history = pd.read_csv(search_history_file)
            st.table(search_history)

        # Add a "Clear History" button to clear the search history
        if st.button("Clear History"):
            # Clear the history by overwriting the CSV file with an empty DataFrame
            pd.DataFrame(columns=["Food", "Calories"]).to_csv(search_history_file, index=False)
            st.success("Search history cleared!")

st.write("Choose your option")
if st.button("Meal Planner"):
    switch_page("app")
if st.button("Deadlift Counter"):
    switch_page("app2")
if st.button("Workout Generator"):
    switch_page("workoutgen")
if st.button("Water Tracker"):
    switch_page("waternotif")