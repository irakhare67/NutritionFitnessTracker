import streamlit as st
import requests
import pandas as pd
import os


st.markdown(
    """
    <style>
    body {
        background-color: #e0ffe0; /* Light green background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Create a Streamlit app for meal planning based on user category
st.title("Meal Planner")

# Sidebar for user category selection
user_category = st.sidebar.selectbox("Select Your Category", ["Weight Loss", "Maintenance", "Muscle Mass Increase", "Bulking"])

# Define meal plans for each category with Indian food
meal_plans = {
    "Weight Loss": {
        "Day 1": ["Breakfast: Upma", "Lunch: Tofu Salad", "Dinner: Grilled Fish"],
        "Day 2": ["Breakfast: Poha", "Lunch: Mixed Vegetable Soup", "Dinner: Lentil Curry"],
        "Day 3": ["Breakfast: Idli with Sambar", "Lunch: Spinach Salad", "Dinner: Baked Chicken"],
        "Day 4": ["Breakfast: Poha", "Lunch: Chickpea Curry", "Dinner: Steamed Broccoli"],
        "Day 5": ["Breakfast: Oats with Almonds", "Lunch: Cucumber Raita", "Dinner: Tofu Stir-Fry"],
        "Day 6": ["Breakfast: Dhokla", "Lunch: Mushroom Soup", "Dinner: Grilled Paneer"],
    },
    "Maintenance": {
        "Day 1": ["Breakfast: Paratha with Curd", "Lunch: Vegetable Biryani", "Dinner: Grilled Fish"],
        "Day 2": ["Breakfast: Aloo Puri", "Lunch: Chana Masala", "Dinner: Chicken Curry"],
        "Day 3": ["Breakfast: Dosa", "Lunch: Paneer Tikka", "Dinner: Vegetable Pulao"],
        "Day 4": ["Breakfast: Sabudana Khichdi", "Lunch: Mixed Dal", "Dinner: Baked Salmon"],
        "Day 5": ["Breakfast: Masala Dosa", "Lunch:  Potato curry", "Dinner: Tofu Stir-Fry"],
        "Day 6": ["Breakfast: Pongal", "Lunch: Palak Paneer", "Dinner: Mushroom Biryani"],
    },
    "Muscle Mass Increase": {
        "Day 1": ["Breakfast: Protein Pancakes", "Lunch: Chicken Biryani", "Dinner: Grilled Mutton"],
        "Day 2": ["Breakfast: Scrambled Eggs", "Lunch:  Chicken Curry", "Dinner: Paneer Tikka"],
        "Day 3": ["Breakfast: Chicken Sandwich", "Lunch: Tofu and Quinoa Salad", "Dinner: Fish Curry"],
        "Day 4": ["Breakfast: Omelette", "Lunch: Chickpea and Rice", "Dinner: Mixed Dal"],
        "Day 5": ["Breakfast: Protein Shake", "Lunch: Egg Fried Rice", "Dinner: Grilled Chicken"],
        "Day 6": ["Breakfast: Chicken Paratha", "Lunch: Beef Biryani", "Dinner: Lentil Soup"],
    },
    "Bulking": {
        "Day 1": ["Breakfast: Aloo Paratha", "Lunch: Mutton Biryani", "Dinner: Butter Chicken"],
        "Day 2": ["Breakfast: Paneer Bhurji", "Lunch: Chole Bhature", "Dinner: Tandoori Lamb"],
        "Day 3": ["Breakfast: Chicken Sandwich", "Lunch: Mutton Korma", "Dinner: Fish Curry"],
        "Day 4": ["Breakfast: Masala Dosa", "Lunch: Rogan Josh", "Dinner: Paneer Tikka"],
        "Day 5": ["Breakfast: Protein Shake", "Lunch: Chicken Biryani", "Dinner: Beef Curry"],
        "Day 6": ["Breakfast: Chicken Paratha", "Lunch: Keema Pav", "Dinner: Mutton Curry"],
    },
}

# API endpoint for nutrition information
url = "https://api.api-ninjas.com/v1/nutrition?query="
headers = {
    "X-API-Key": "cSNXvt31N7FSRia1HJfJlg==j3XuZh8S3Cw6Aqwg"
}

# Initialize total nutrition for each day and week
total_nutrition = {
    "Calories": [0, 0],
    "Fat (Total)": [0, 0],
    "Fat (Saturated)": [0, 0],
    "Protein": [0, 0],
    "Carbohydrates": [0, 0],
    "Fiber": [0, 0],
    "Sugar": [0, 0],
}

# Display the meal plan for the selected category
if user_category:
    st.header(f"Your {user_category} Meal Plan")
    st.write("Follow this meal plan for 6 days and enjoy a cheat day on the 7th day!")

    # Create a DataFrame to store nutrition information for each food item
    daily_nutrition_data = []

    if user_category in meal_plans:
        for day, options in meal_plans[user_category].items():
            st.subheader(day)
            daily_calories = 0
            daily_nutrition = {
                "Calories": 0,
                "Fat (Total)": 0,
                "Fat (Saturated)": 0,
                "Protein": 0,
                "Carbohydrates": 0,
                "Fiber": 0,
                "Sugar": 0,
            }

            # Create lists to store food items for breakfast, lunch, and dinner
            breakfast_items = []
            lunch_items = []
            dinner_items = []

            for option in options:
                if not option.startswith("Day 7 (Cheat Day)"):
                    if option.startswith("Breakfast:"):
                        food_item = option.split(":")[1].strip()
                        # Make an API request to get nutrition information
                        response = requests.get(url + food_item, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            if result:
                                food_info = result[0]  # Take the first result
                                food_item_info = {
                                    "Food Item": food_item,
                                    "Calories": food_info.get("calories", 0),
                                    "Fat (Total)": food_info.get("fat_total_g", 0),
                                    "Fat (Saturated)": food_info.get("fat_saturated_g", 0),
                                    "Protein": food_info.get("protein_g", 0),
                                    "Carbohydrates": food_info.get("carbohydrates_total_g", 0),
                                    "Fiber": food_info.get("fiber_g", 0),
                                    "Sugar": food_info.get("sugar_g", 0),
                                }
                                breakfast_items.append(food_item_info)
                                daily_nutrition["Calories"] += food_info.get("calories", 0)
                                daily_nutrition["Fat (Total)"] += food_info.get("fat_total_g", 0)
                                daily_nutrition["Fat (Saturated)"] += food_info.get("fat_saturated_g", 0)
                                daily_nutrition["Protein"] += food_info.get("protein_g", 0)
                                daily_nutrition["Carbohydrates"] += food_info.get("carbohydrates_total_g", 0)
                                daily_nutrition["Fiber"] += food_info.get("fiber_g", 0)
                                daily_nutrition["Sugar"] += food_info.get("sugar_g", 0)
                            else:
                                st.warning(f"No nutrition information found for {food_item}")
                        else:
                            st.warning(f"Error getting nutrition information for {food_item}")
                            st.write(f"API Response: {response.text}")
                    elif option.startswith("Lunch:"):
                        food_item = option.split(":")[1].strip()
                        # Make an API request to get nutrition information
                        response = requests.get(url + food_item, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            if result:
                                food_info = result[0]  # Take the first result
                                food_item_info = {
                                    "Food Item": food_item,
                                    "Calories": food_info.get("calories", 0),
                                    "Fat (Total)": food_info.get("fat_total_g", 0),
                                    "Fat (Saturated)": food_info.get("fat_saturated_g", 0),
                                    "Protein": food_info.get("protein_g", 0),
                                    "Carbohydrates": food_info.get("carbohydrates_total_g", 0),
                                    "Fiber": food_info.get("fiber_g", 0),
                                    "Sugar": food_info.get("sugar_g", 0),
                                }
                                lunch_items.append(food_item_info)
                                daily_nutrition["Calories"] += food_info.get("calories", 0)
                                daily_nutrition["Fat (Total)"] += food_info.get("fat_total_g", 0)
                                daily_nutrition["Fat (Saturated)"] += food_info.get("fat_saturated_g", 0)
                                daily_nutrition["Protein"] += food_info.get("protein_g", 0)
                                daily_nutrition["Carbohydrates"] += food_info.get("carbohydrates_total_g", 0)
                                daily_nutrition["Fiber"] += food_info.get("fiber_g", 0)
                                daily_nutrition["Sugar"] += food_info.get("sugar_g", 0)
                            else:
                                st.warning(f"No nutrition information found for {food_item}")
                        else:
                            st.warning(f"Error getting nutrition information for {food_item}")
                            st.write(f"API Response: {response.text}")
                    elif option.startswith("Dinner:"):
                        food_item = option.split(":")[1].strip()
                        # Make an API request to get nutrition information
                        response = requests.get(url + food_item, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            if result:
                                food_info = result[0]  # Take the first result
                                food_item_info = {
                                    "Food Item": food_item,
                                    "Calories": food_info.get("calories", 0),
                                    "Fat (Total)": food_info.get("fat_total_g", 0),
                                    "Fat (Saturated)": food_info.get("fat_saturated_g", 0),
                                    "Protein": food_info.get("protein_g", 0),
                                    "Carbohydrates": food_info.get("carbohydrates_total_g", 0),
                                    "Fiber": food_info.get("fiber_g", 0),
                                    "Sugar": food_info.get("sugar_g", 0),
                                }
                                dinner_items.append(food_item_info)
                                daily_nutrition["Calories"] += food_info.get("calories", 0)
                                daily_nutrition["Fat (Total)"] += food_info.get("fat_total_g", 0)
                                daily_nutrition["Fat (Saturated)"] += food_info.get("fat_saturated_g", 0)
                                daily_nutrition["Protein"] += food_info.get("protein_g", 0)
                                daily_nutrition["Carbohydrates"] += food_info.get("carbohydrates_total_g", 0)
                                daily_nutrition["Fiber"] += food_info.get("fiber_g", 0)
                                daily_nutrition["Sugar"] += food_info.get("sugar_g", 0)
                            else:
                                st.warning(f"No nutrition information found for {food_item}")
                        else:
                            st.warning(f"Error getting nutrition information for {food_item}")
                            st.write(f"API Response: {response.text}")

            # Display food items and their details for breakfast, lunch, and dinner
            if breakfast_items:
                st.write("Breakfast Items:")
                st.table(pd.DataFrame(breakfast_items))
            if lunch_items:
                st.write("Lunch Items:")
                st.table(pd.DataFrame(lunch_items))
            if dinner_items:
                st.write("Dinner Items:")
                st.table(pd.DataFrame(dinner_items))

            # Display the daily nutrition information in a table
            st.write("Daily Nutrition Total:")
            st.table(pd.DataFrame([daily_nutrition]))

            daily_nutrition_data.append(daily_nutrition)

       
   
# Create a section for the Day 7 meal
st.header("Day 7 Meal")

# Read the search history from the CSV file
search_history_file = "search_history.csv"
if os.path.exists(search_history_file):
    search_history = pd.read_csv(search_history_file)
else:
    search_history = pd.DataFrame(columns=["Food", "Calories"])

# ... (previous code)

# Create a section for the Day 7 meal


# Read the search history from the CSV file

# Read the search history from the CSV file
search_history_file = "search_history.csv"
if os.path.exists(search_history_file):
    search_history = pd.read_csv(search_history_file)
else:
    search_history = pd.DataFrame(columns=["Food", "Calories"])

# Create a list to store food items for Day 7
day_7_items = []

# Create a checkbox to include custom meals
include_custom_meal = st.checkbox("Include Custom Meals for Day 7")

if include_custom_meal:
    custom_meals = st.multiselect("Select Food Items from Search History", search_history["Food"].tolist())
    for custom_meal in custom_meals:
        st.write("Custom Meal:")
        st.write(f"- {custom_meal}")

        # Make an API request to get nutrition information for the custom meal
        response = requests.get(url + custom_meal, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result:
                food_info = result[0]  # Take the first result
                day_7_items.append({
                    "Food Item": custom_meal,
                    "Calories": food_info.get("calories", 0),
                    "Fat (Total)": food_info.get("fat_total_g", 0),
                    "Fat (Saturated)": food_info.get("fat_saturated_g", 0),
                    "Protein": food_info.get("protein_g", 0),
                    "Carbohydrates": food_info.get("carbohydrates_total_g", 0),
                    "Fiber": food_info.get("fiber_g", 0),
                    "Sugar": food_info.get("sugar_g", 0),
                })
            else:
                st.warning(f"No nutrition information found for {custom_meal}")
        else:
            st.warning(f"Error getting nutrition information for {custom_meal}")
            st.write(f"API Response: {response.text}")

# Create a checkbox to display the daily nutrition table for Day 7
show_day_7_nutrition = st.checkbox("Show Daily Nutrition for Day 7")

if show_day_7_nutrition:
    st.write("Daily Nutrition for Day 7:")
    day_7_nutrition_df = pd.DataFrame(day_7_items)
    st.table(day_7_nutrition_df)






# ... (rest of the code, including the meal plan)

daily_nutrition_df = pd.DataFrame(daily_nutrition_data)

for key, values in total_nutrition.items():
    total_nutrition[key][0] = daily_nutrition_df[key].sum()

# Add Day 7 nutrition to the weekly total
for item in day_7_items:
    for key in total_nutrition.keys():
        total_nutrition[key][0] += item[key]

st.write("-" * 50)
st.write("Weekly Nutrition Total:")
weekly_total = {
    "Calories": total_nutrition["Calories"][0],  # Weekly total
    "Fat (Total)": total_nutrition["Fat (Total)"][0],  # Weekly total
    "Fat (Saturated)": total_nutrition["Fat (Saturated)"][0],  # Weekly total
    "Protein": total_nutrition["Protein"][0],  # Weekly total
    "Carbohydrates": total_nutrition["Carbohydrates"][0],  # Weekly total
    "Fiber": total_nutrition["Fiber"][0],  # Weekly total
    "Sugar": total_nutrition["Sugar"][0],  # Weekly total
}
st.table(pd.DataFrame([weekly_total]))