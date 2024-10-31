import streamlit as st
import base64
from datetime import datetime

def survey_section():
    st.header("User Feedback Survey")

    # User Name Input
    user_name = st.text_input("Enter your name:")

    # Date Input for next workout planning
    next_workout_date = st.date_input("Select your next workout date:")

    # Upload an image of the workout
    workout_image = st.file_uploader("Upload an image of your workout (optional):", type=["jpg", "jpeg", "png"])

    # Weight recorded
    weight_recorded = st.number_input("Enter your weight (in kg):", min_value=0.0)

    # Max heart rate recorded
    max_heart_rate = st.number_input("Enter your max heart rate (in bpm):", min_value=0)

    # Checkboxes for body parts triggered
    body_parts = st.multiselect(
        "Which body parts did you focus on today?",
        ["Arms", "Legs", "Back", "Chest", "Core", "Shoulders"]
    )

    # Feelings after exercise
    feelings = st.selectbox(
        "How do you feel after exercising?",
        ["Very Good", "Good", "Neutral", "Bad", "Very Bad"]
    )

    # Muscle workout intensity
    muscle_workout = st.slider(
        "How much do you think your muscles are worked out?",
        0, 10, 5  # Scale from 0 (not at all) to 10 (extremely)
    )

    # Feelings about doing the exercise
    exercise_feeling = st.selectbox(
        "How do you feel about doing this exercise?",
        ["Excited", "Motivated", "Indifferent", "Tired", "Dread"]
    )

    # Option to record pain
    record_pain = st.radio(
        "Do you want to record any pain?",
        ["Yes", "No"]
    )

    # If user wants to record pain, provide an input field
    pain_description = ""
    if record_pain == "Yes":
        pain_description = st.text_area("Please describe the pain (optional):")

    # Submit button for the survey
    if st.button("Submit Survey"):
        if user_name:  # Check if user_name is provided
            # Prepare the data to be inserted
            survey_data = {
                "name": user_name,
                "next_workout_date": str(next_workout_date),
                "weight": weight_recorded,
                "heart_rate": max_heart_rate,
                "intensity": muscle_workout,
                "body_parts": body_parts,
                "feelings": feelings,
                "exercise_feeling": exercise_feeling,
                "pain": pain_description,
            }

            # Handle image upload
            if workout_image is not None:
                # Encode image to base64
                img_bytes = workout_image.read()  # Read the image bytes
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')  # Encode as base64 string
                survey_data["workout_image"] = img_base64  # Add base64 image to survey data

                # Optionally, display the uploaded image
                st.image(workout_image, caption="Uploaded Workout Image", use_column_width=True)

            # Display survey results
            st.write(f"Name: {user_name}")
            st.write(f"Next Workout Date: {next_workout_date}")
            if workout_image is not None:
                st.image(workout_image, caption="Uploaded Workout Image", use_column_width=True)
            st.write(f"Weight Recorded: {weight_recorded} kg")
            st.write(f"Max Heart Rate Recorded: {max_heart_rate} bpm")
            st.write(f"Body Parts Focused: {', '.join(body_parts)}")
            st.write(f"Feelings after Exercise: {feelings}")
            st.write(f"Muscle Workout Intensity: {muscle_workout}")
            st.write(f"Feelings about the Exercise: {exercise_feeling}")
            if record_pain == "Yes":
                st.write(f"Pain Description: {pain_description}")

            return survey_data
