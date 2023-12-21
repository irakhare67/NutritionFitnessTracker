import streamlit as st
import random

# Exercise lists
cardio_exercises = [
    "Running", "Jumping jacks", "Cycling", "Swimming", "Jump rope", "Burpees",
    "Boxing", "High knees", "Mountain climbers", "Sprint intervals", "Rowing",
    "Hiking", "Aerobic dance", "Elliptical machine", "Crossfit", "Stair climbing",
    "Kickboxing", "Hula hooping", "In-line skating", "Basketball",
]

strength_exercises = [
    "Push-ups", "Squats", "Planks", "Dumbbell curls", "Lunges", "Bench press",
    "Deadlifts", "Pull-ups", "Leg press", "Bicep curls", "Tricep dips",
    "Russian twists", "Shoulder press", "Wall sit", "Lateral raises",
    "Leg curls", "Calf raises", "Kettlebell swings", "Barbell rows", "Hammer curls",
]

flexibility_exercises = [
    "Yoga", "Pilates", "Stretching", "Tai Chi", "Foam rolling", "Pigeon pose",
    "Butterfly stretch", "Child's pose", "Cobra stretch", "Cat-cow stretch",
    "Standing quad stretch", "Seated forward bend", "Triangle pose", "Sphinx pose",
    "Bridge pose", "Shoulder bridge", "Thread the needle", "Happy baby pose", "Reclining hand-to-big-toe pose",
]

balance_exercises = [
    "Balance board", "Single-leg stance", "Bosu ball exercises", "Stork stand", "Heel-to-toe walk",
    "Standing ankle circles", "Tree pose", "Warrior III pose", "One-legged deadlift", "Rock the boat",
    "Tightrope walk", "Chair pose", "Eagle pose", "Half moon pose", "Scale pose",
    "Crow pose", "One-legged balance reach", "Yoga balance sequence", "Supine twist", "King Pigeon pose",
]

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_meters = height / 100
    return weight / (height_meters ** 2)

# Function to generate a workout plan with assigned time
def generate_workout(weight, height, requirements, total_time, num_exercises):
    workout_plan = []
    time_per_exercise = total_time / num_exercises

    if "cardio" in requirements:
        cardio_sample = random.sample(cardio_exercises, num_exercises)
        workout_plan.extend((exercise, time_per_exercise) for exercise in cardio_sample)

    if "strength" in requirements:
        strength_sample = random.sample(strength_exercises, num_exercises)
        workout_plan.extend((exercise, time_per_exercise) for exercise in strength_sample)

    if "flexibility" in requirements:
        flexibility_sample = random.sample(flexibility_exercises, num_exercises)
        workout_plan.extend((exercise, time_per_exercise) for exercise in flexibility_sample)

    if "balance" in requirements:
        balance_sample = random.sample(balance_exercises, num_exercises)
        workout_plan.extend((exercise, time_per_exercise) for exercise in balance_sample)

    random.shuffle(workout_plan)
    return workout_plan

# Function to provide a short message based on BMI
def bmi_message(bmi):
    if bmi < 18.5:
        return "You are underweight. Maintain a healthy weight."
    elif 18.5 <= bmi < 25:
        return "Your weight is healthy. Keep it up!"
    elif 25 <= bmi < 30:
        return "You are overweight. Consider regular exercise."
    else:
        return "You are obese. Focus on a healthy diet and exercise."

# Function to create a workout schedule
def create_workout_schedule(weight, height, requirements, active_days, total_time, num_exercises):
    schedule = {}
    
    for day in range(1, int(active_days) + 1):
        workout = generate_workout(weight, height, requirements, total_time, int(num_exercises))
        schedule[f"Day {day}"] = workout

    return schedule

# Set a background image
# Set Streamlit theme to change text color to white
st.markdown(
    """
    <style>
    .stTextInput, .stNumberInput, .stTextArea, .stSelectbox, .stButton {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exercise lists
# ...

# Function to calculate BMI
# ...

# Function to generate a workout plan with assigned time
# ...

# Function to provide a short message based on BMI
# ...

# Function to create a workout schedule
# ...

# Set a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://wallpapercosmos.com/w/full/9/0/1/266063-3840x2160-desktop-4k-fitness-wallpaper-image.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app
def main():
    st.markdown("<h1 style='color: white;'>Personal Workout Planner</h1>", unsafe_allow_html=True)

    weight = st.number_input("Weight (kg):", value=70.0)
    height = st.number_input("Height (cm):", value=170.0)
    requirements = st.text_input("Workout requirements (e.g., strength, flexibility, balance, cardio):").split()
    active_days = st.number_input("Active days per week:", value=3.0)
    total_time = st.number_input("Total workout time per day (minutes):", value=90.0)
    num_exercises = st.number_input("Number of exercises to assign (2-5):", value=2.0)

    if st.button("Generate Workout"):
        if not (2 <= num_exercises <= 5):
            st.error("Number of exercises must be between 2 and 5.")
        else:
            bmi = calculate_bmi(weight, height)
            schedule = create_workout_schedule(weight, height, requirements, active_days, total_time, num_exercises)

            # Display the BMI and a short message based on BMI
            st.subheader(f"BMI: {bmi:.2f}")
            st.write(f"Message: {bmi_message(bmi)}")

            if not schedule:
                st.warning("No workout schedule generated. Please check your input values.")
            else:
                # Display the workout schedule
                for day, workout in schedule.items():
                    st.subheader(f"{day} Workout Plan:")
                    for i, (exercise, time) in enumerate(workout, start=1):
                        st.write(f"{i}. {exercise}: {time} minutes")

if __name__ == "__main__":
    main()