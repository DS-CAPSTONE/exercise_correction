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
import av
skeleton_img = get_static_file_url("assets/skeleton.jpg")
import base64
import time
import cv2
import streamlit as st
import random
from gtts import gTTS
import tempfile
from pydub import AudioSegment



# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Motivational messages
motivational_messages = [
    "Welcome to the app! Remember to do the exercise properly.",
    "You can do it! Stay focused and keep moving.",
    "Great to have you here! Every step counts.",
    "Believe in yourself! You are stronger than you think.",
    "Let's get moving! Your effort today leads to results tomorrow.",
    "Stay positive! Progress is progress, no matter how small.",
    "You've got this! Every moment is an opportunity to improve.",
    "Keep pushing your limits! Challenge yourself to do better.",
    "Success starts with the first step. Let’s take it together!",
    "Your journey is unique. Embrace every moment of it!",
    "Stay committed! Your hard work will pay off in the end.",
    "Great things take time. Keep at it, and you’ll see results!",
    "Remember, your only competition is yourself. Be the best you can be!",
    "Focus on the process, not just the results. Enjoy the journey!",
    "The only bad workout is the one that didn’t happen.",
    "Stay strong! Each day is a new chance to improve.",
    "Consistency is key. Keep showing up, and you will get there!",
    "Push through the tough times! They will make you stronger.",
    "Every drop of sweat brings you closer to your goals.",
    "Stay motivated! You are capable of achieving amazing things.",
    "Visualize your success! Picture yourself reaching your goals.",
    "Embrace the challenge! It’s what helps you grow.",
    "The journey may be tough, but so are you! Keep going.",
    "Celebrate your victories, no matter how small. They matter!",
    "Dedication and persistence lead to success. You’ve got this!",
    "Your body can stand almost anything. It’s your mind that you have to convince.",
    "You are not alone on this journey. We're in this together!",
    "Don’t just aim to be better than others; aim to be better than you were yesterday.",
    "Let your determination be stronger than your excuses.",
    "Stay committed to your goals, and the results will follow.",
    "Every day is an opportunity to improve yourself. Take it!",
    "You're making progress even on days when you feel like you’re not.",
    "Keep your head up and your heart strong. You're on the right path!",
    "You have the power to change your story. Start today!",
    "Believe in your abilities. You are capable of great things!",
    "Make today count! You won't get this day back.",
    "You are one workout away from a better mood. Let’s do this!",
    "Let’s crush those goals together! One step at a time.",
    "Your effort is a reflection of your dedication. Keep it up!",
    "Progress, not perfection, is the goal. Keep moving forward.",
    "Your mindset is everything. Choose positivity!",
    "Every rep counts, and every step brings you closer.",
    "Embrace the discomfort! It’s where the growth happens.",
    "Stay hungry for success! You are just getting started.",
    "You are stronger than your strongest excuse. Don’t let it win!",
    "Your potential is limitless! Keep striving for greatness.",
    "This is your moment! Own it and make the most of it.",
    "Success is the sum of small efforts repeated day in and day out."
]


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

# Define body part regions
body_parts = {
    "Head (Front)": (0, 0, 300, 100),
    "Left Shoulder (Front)": (50, 100, 150, 150),
    "Right Shoulder (Front)": (150, 100, 250, 150),
    "Chest": (75, 150, 225, 200),
    "Abdomen": (100, 200, 200, 300),
    "Left Arm (Front)": (0, 150, 75, 400),
    "Right Arm (Front)": (225, 150, 300, 400),
    "Hips": (100, 300, 200, 350),
    "Left Leg (Front)": (50, 350, 150, 587),
    "Right Leg (Front)": (150, 350, 250, 587),
    "Head (Back)": (310, 0, 500, 100),
    "Left Shoulder (Back)": (360, 100, 410, 150),
    "Right Shoulder (Back)": (450, 100, 500, 150),
    "Upper Back": (360, 150, 468, 180),
    "Middle Back": (370, 180, 468, 266),
    "Left Arm (Back)": (310, 150, 360, 400),
    "Right Arm (Back)": (500, 150, 550, 400),
    "Glutes": (360, 266, 475, 350),
    "Left Leg (Back)": (300, 350, 420, 587),
    "Right Leg (Back)": (420, 350, 550, 587)
}

# Function to identify body part based on coordinates
def identify_body_part(x, y):
    for part, (x_min, y_min, x_max, y_max) in body_parts.items():
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return part
    return "Unknown"

# Define body part to exercise recommendations
exercise_recommendations = {
    "Head (Front)": ["Neck stretches", "Shoulder shrugs", "Head rotations"],
    "Left Shoulder (Front)": ["Shoulder rolls", "Arm circles", "Pendulum stretch"],
    "Right Shoulder (Front)": ["Shoulder rolls", "Arm circles", "Pendulum stretch"],
    "Chest": ["Chest stretch", "Arm pull stretch", "Wall push-ups"],
    "Abdomen": ["Pelvic tilts", "Seated knee lifts", "Core twist stretches"],
    "Left Arm (Front)": ["Wrist flexor stretch", "Bicep curls", "Arm stretches"],
    "Right Arm (Front)": ["Wrist flexor stretch", "Bicep curls", "Arm stretches"],
    "Hips": ["Hip flexor stretch", "Standing leg raises", "Knee-to-chest stretch"],
    "Left Leg (Front)": ["Quad stretch", "Calf raises", "Seated hamstring stretch"],
    "Right Leg (Front)": ["Quad stretch", "Calf raises", "Seated hamstring stretch"],
    "Head (Back)": ["Neck extensions", "Shoulder blade squeeze", "Head tilts"],
    "Left Shoulder (Back)": ["Shoulder blade squeeze", "Backward arm circles", "Scapula stretch"],
    "Right Shoulder (Back)": ["Shoulder blade squeeze", "Backward arm circles", "Scapula stretch"],
    "Upper Back": ["Cat-cow stretch", "Child's pose", "Thoracic extension"],
    "Middle Back": ["Seated twist", "Lat stretch", "Back rotations"],
    "Left Arm (Back)": ["Tricep stretches", "Wrist flexor stretch", "Arm circles"],
    "Right Arm (Back)": ["Tricep stretches", "Wrist flexor stretch", "Arm circles"],
    "Glutes": ["Pigeon stretch", "Seated figure-four stretch", "Glute bridges"],
    "Left Leg (Back)": ["Hamstring stretch", "Lunges", "Calf raises"],
    "Right Leg (Back)": ["Hamstring stretch", "Lunges", "Calf raises"]
}

# Function to suggest an exercise based on the paining body part
def suggest_exercise(body_part):
    exercises = exercise_recommendations.get(body_part)
    if exercises:
        return random.choice(exercises)
    else:
        return "No exercise recommendation available for this body part."



def preprocess_image(image):
    """Preprocess the image (resize, convert color)."""
    resized_image = cv2.resize(image, (224, 224))
    return resized_image

pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
def video_frame_callback(frame: av.VideoFrame, selected_exercise):
    """Callback to process each video frame and run the selected model."""
    # We got the video.
    # Assume `frame` is your video frame in YUV format
    # frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)

    img = frame.to_ndarray(format="bgr24")
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # Preprocess image
    image.flags.writeable = False

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
        detection = exercise_model.detect(mp_results=results, image=image, timestamp=frame.time)
        pass


    return av.VideoFrame.from_ndarray(image, format="bgr24")


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


# Login Section
def login():
    if "user_name" not in st.session_state:
        # Sidebar login section
        with st.sidebar:
            st.markdown("### Please log in to continue.")
            user_name = st.text_input("Enter your name:", key="user_name_input")
            login_button = st.button("Login")

            if login_button and user_name:
                st.session_state["user_name"] = user_name
                st.sidebar.success(f"Welcome, {user_name}!")
                st.rerun()

                # Refresh to update login status
            elif login_button and not user_name:
                st.error("Please enter your name to log in.")

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def play_welcome_message(message):
    # Generate audio from the message
    tts = gTTS(text=message, lang='en')

    # Use a temporary file to store the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts.save(tmp_file.name)
        # Use Streamlit's audio component to play the audio file
        autoplay_audio(tmp_file.name)
        # Load the audio file to calculate duration
        audio = AudioSegment.from_file(tmp_file.name)
        duration_in_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
        return duration_in_seconds

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
    # Display main title
    st.title("Real-Time Exercise Posture Correction App")
    st.sidebar.title("Exercise Detection Models")

    ## Only show the main app content if user is logged in
    if "user_name" in st.session_state:
        # Main app content
        st.write(f"Hello, {st.session_state['user_name']}! Start your exercise session.")
        # Generate the welcome message
        motivation = random.choice(motivational_messages)
        welcome_message = f"Welcome, {st.session_state['user_name']}!,  {motivation}"

        # Convert the welcome message to speech
        play_welcome_message(welcome_message)
        # Play the audio automatically using HTML

    else:
        login()
        st.write("Please log in to continue.")
        return


    # Sidebar - Select Exercise Model
    choice = st.sidebar.selectbox("Select Exercise", list(exercise_models.keys()))

    # Sidebar - Chat with ChatGPT
    st.sidebar.title("Chat with AI TRAINER")
    user_input = st.sidebar.text_area("Ask a question:", placeholder="Type here...")

    # Send user input to ChatGPT and get response
    response_ai = None
    if st.sidebar.button("Get Response"):
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=100
            )
            # Display the response correctly
            st.sidebar.write("TRAINER says:", response['choices'][0]['message']['content'].strip())
            response_ai = response['choices'][0]['message']['content'].strip()

    if response_ai:

        seconds_total = play_welcome_message(response_ai)
        time.sleep(seconds_total+1)


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
            video_frame_callback=lambda frame: video_frame_callback(frame, choice),
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
        part = identify_body_part(x, y)
        st.write(f"Latest Clicked Point - x: {x}, y: {y} part: {part}")
        recommended_exercise = suggest_exercise(part)
        st.write(f"Recommended exercise for paining {part}: {recommended_exercise}")

    survey_section()

if __name__ == "__main__":
    main()
