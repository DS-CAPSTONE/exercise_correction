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
openai.api_key = 'your_openai_api_key'  # replace with your API key


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

def main():
    st.title("Real-Time Exercise Posture Correction App")
    st.sidebar.title("Exercise Detection Models")

    # Sidebar - Select Exercise Model
    choice = st.sidebar.selectbox("Select Exercise", list(exercise_models.keys()))

    # Sidebar - Chat with ChatGPT
    st.sidebar.title("Chat with GPT")
    user_input = st.sidebar.text_area("Ask a question:", placeholder="Type here...")

    # Send user input to ChatGPT and get response
    if st.sidebar.button("Get Response"):
        if user_input:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=user_input,
                max_tokens=100
            )
            st.sidebar.write("GPT says:", response.choices[0].text.strip())

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
    skeleton_img = get_static_file_url("assets/skeleton.jpg")


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

if __name__ == "__main__":
    main()
