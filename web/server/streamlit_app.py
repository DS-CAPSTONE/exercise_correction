import streamlit as st
from streamlit_drawable_canvas import st_canvas
import av
from PIL import Image
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import mediapipe as mp
from detection_realtime.plank import PlankDetection
from detection_realtime.bicep_curl import BicepCurlDetection
from detection_realtime.squat import SquatDetection
from detection_realtime.lunge import LungeDetection
import sys
import os
import openai
from detection_realtime.utils import (
    get_static_file_url
)

import cv2


# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Drawing helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize models
exercise_models = {
    "Plank": PlankDetection(),
    "Bicep Curl": BicepCurlDetection(),
    "Squat": SquatDetection(),
    "Lunge": LungeDetection(),
}
# Initialize OpenAI API
openai.api_key = "sk-proj-Xzh04" + "rXHHRmzJr4L6d4mYAtivOvAu-j8I5-v5Tan0" + "-6ndPqD-14aw84PYbVH_Gnx86Pwe9FctnT3BlbkFJQiJjPIbtrTn" + "LZdP0cxTYdPu_B82tpq3dEcMRoMWMqkNf1uzRLhg4P91OpdqNpz7VniVUgeFbwA"  # replace with your API key


def preprocess_image(image):
    """Preprocess the image (resize, convert color)."""
    resized_image = cv2.resize(image, (224, 224))
    return resized_image


def video_frame_callback(frame: av.VideoFrame, selected_exercise):
    """Callback to process each video frame and run the selected model."""
    # We got the video.
    # Assume `frame` is your video frame in YUV format
    # frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)

    img = frame.to_ndarray(format="bgr24")
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # Preprocess image
    image.flags.writeable = False
    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Drawing landmarks
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(244, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=1),
        )



        # Apply the selected model
        exercise_model = exercise_models.get(selected_exercise)
        if results.pose_landmarks:
            detection = exercise_model.detect(mp_results=results, image=image)
        else:
            top_left = (50, 50)  # Top-left corner of the rectangle
            bottom_right = (300, 200)  # Bottom-right corner of the rectangle
            color = (0, 255, 0)  # Rectangle color (Green)
            thickness = 2  # Thickness of the rectangle border

            # Draw the rectangle on the frame
            img = cv2.rectangle(img, top_left, bottom_right, color, thickness)

            # Add the exercise type as a label
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (255, 0, 0)  # Font color (Blue)
            font_thickness = 2
            text_position = (60, 40)  # Position of the label

            # Put the text label on the frame
            cv2.putText(img, selected_exercise, text_position, font, font_scale, font_color, font_thickness)


    return av.VideoFrame.from_ndarray(image, format="bgr24")

import av
import cv2
import numpy as np
skeleton_img = get_static_file_url("assets/skeleton.jpg")

def video_frame_callback_fake(frame, exercise_type):
    img = frame.to_ndarray(format="bgr24")  # Convert the frame to a numpy array

    # Define rectangle parameters
    top_left = (50, 50)  # Top-left corner of the rectangle
    bottom_right = (300, 200)  # Bottom-right corner of the rectangle
    color = (0, 255, 0)  # Rectangle color (Green)
    thickness = 2  # Thickness of the rectangle border

    # Draw the rectangle on the frame
    img = cv2.rectangle(img, top_left, bottom_right, color, thickness)

    # Add the exercise type as a label
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 0, 0)  # Font color (Blue)
    font_thickness = 2
    text_position = (60, 40)  # Position of the label

    # Put the text label on the frame
    cv2.putText(img, exercise_type, text_position, font, font_scale, font_color, font_thickness)

    # Return the modified frame
    return av.VideoFrame.from_ndarray(img, format="bgr24")

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
        if user_name:
            st.success("Thank you for your feedback!")
            # Displaying the survey data
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
        else:
            st.error("Please enter your name before submitting.")


def main():
    st.markdown(
        """
        <style>
        /* Tinted gradient background */
        .main {
            background: linear-gradient(135deg, rgba(240, 255, 240, 1), rgba(200, 255, 200, 0.7));
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Real-Time Exercise Posture Correction App")
    st.sidebar.title("Exercise Detection Models")

    # Sidebar - Select Exercise Model
    choice = st.sidebar.selectbox("Select Exercise", list(exercise_models.keys()))

    # Sidebar - Chat with ChatGPT
    st.sidebar.title("Chat with AI TRAINER")
    user_input = st.sidebar.text_area("Ask a question:", placeholder="Type here...")

    # Send user input to ChatGPT and get response
    if st.sidebar.button("Get Response"):
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=100
            )
            # Display the response correctly
            st.sidebar.write("TRAINER says:", response['choices'][0]['message']['content'].strip())

    # Main Screen for Exercise Posture Correction
    if choice == "Home":
        st.write("Welcome to the Exercise Posture Correction App.")
        st.write("""
                    This app will help you correct your posture in real-time.
                    Choose an exercise model from the sidebar.
                """)


    elif choice != "Home":
        st.header("Webcam Live Feed")
        st.write("Click on start to use the webcam and check for posture correction.")

        webrtc_streamer(
            key="posture-correction",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            video_frame_callback=lambda frame: video_frame_callback_fake(frame, choice),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=False,
        )

    # Skeleton Image for Pain Detection
    st.header("Pain Detection System")
    st.write("Click on the skeleton image to indicate pain areas during exercise.")


    # Using Streamlit's image click function for pain detection
    # st.image(skeleton_img, use_column_width=True)
    # You could use a JavaScript or custom overlay for capturing clicks on body areas
    # Here you would add the logic to store pain points based on clicks

    # Load image as background for the canvas
    img = Image.open(skeleton_img)
    # Set canvas dimensions
    canvas_result = st_canvas(
        background_image=img,
        fill_color="rgba(0, 0, 0, 0)",  # Transparent fill color
        stroke_width=0,  # No stroke for dots
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="point",  # Mode for capturing clicks
        key="pain_canvas"
    )

    # Initialize session state for coordinates if not already done
    if "coordinates" not in st.session_state:
        st.session_state["coordinates"] = (None, None)

    # Display clicked points
    if canvas_result.json_data is not None:
        for obj in canvas_result.json_data["objects"]:
            # Extract x and y coordinates
            x, y = obj["left"], obj["top"]

            # Update session state with new coordinates
            st.session_state["coordinates"] = (x, y)

    # Display the latest coordinates
    if st.session_state["coordinates"] != (None, None):
        x, y = st.session_state["coordinates"]
        st.write(f"Latest Clicked Point - x: {x}, y: {y}")

    survey_section()

if __name__ == "__main__":
    main()
