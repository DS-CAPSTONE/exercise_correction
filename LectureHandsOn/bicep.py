from datetime import datetime

import streamlit as st
import av
import cv2
import torch
from transformers import pipeline
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# Load the emotion classification model from Hugging Face
device = "cpu"  # You can switch to "mps" if you're on an M1 Mac and want to use the Apple GPU.
emotion_classifier = pipeline("image-classification", model="dima806/facial_emotions_image_detection", device=device)


# Function to preprocess the image (resize and format the image)
def preprocess_image(image):
    resized_image = cv2.resize(image, (224, 224))  # Resize to 224x224
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)  # Convert to RGB (required by most models)
    return rgb_image

# Define the callback for each frame
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    # Preprocess the image for the bicep curl posture correction (placeholder)
    preprocessed_img = preprocess_image(img)

    # Perform bicep curl posture correction prediction (future implementation)
    try:
        prediction = "temp"  # Placeholder for bicep curl model integration
        predicted_label = str(datetime.now())  # Current timestamp for now
        st.write(f"Predicted Posture Correction Time: {predicted_label}")

        # Draw the predicted label (timestamp) on the frame
        cv2.putText(img, f"Timestamp: {predicted_label}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    except Exception as e:
        st.error(f"Error in prediction: {e}")

    return av.VideoFrame.from_ndarray(img, format="bgr24")


# Streamlit app main interface
def main():
    st.title("Real-Time Bicep Curl Posture Correction Application")

    activities = ["Home", "Webcam Posture Correction"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "Home":
        st.write("Welcome to the Bicep Curl Posture Correction App.")
        st.write("""
            This app will help correct your bicep curl posture in real-time using your webcam. 
            Currently, the model is under development. For now, the app shows the timestamps of video frames.
        """)

    elif choice == "Webcam Posture Correction":
        st.header("Webcam Live Feed")
        st.write("Click on start to use the webcam and check for posture correction (future feature).")

        webrtc_streamer(
            key="posture-correction",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=False,
        )


if __name__ == "__main__":
    main()
