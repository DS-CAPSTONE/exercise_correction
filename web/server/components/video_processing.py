import cv2
import mediapipe as mp
from detection_realtime.plank import PlankDetection
from detection_realtime.bicep_curl import BicepCurlDetection
from detection_realtime.squat import SquatDetection
from detection_realtime.lunge import LungeDetection
import base64
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time
from components import speech
import streamlit as st

# Drawing helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)

exercise_models = {
    "Plank": PlankDetection(),
    "Bicep Curl": BicepCurlDetection(),
    "Squat": SquatDetection(),
    "Lunge": LungeDetection(),
}

# Global list to store exercise data and frames
# exercise_data_collection = []  # This will collect data across frames


def extract_landmarks(landmarks):
    """Extract landmarks into a list."""
    if landmarks is not None:
        return [(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks.landmark]
    return []  # Return empty list if no landmarks

import time
import threading
from queue import Queue
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# Global variables to control error message timing
last_error_time = 0  # Keeps track of the last error message timestamp
ERROR_DELAY = 10  # Minimum delay in seconds between error messages

# Queue to handle speech messages
speech_queue = Queue()

def play_message_in_background(message):
    """Function to play speech in a separate thread."""
    while not speech_queue.empty():
        message = speech_queue.get()
        # Ensure your speech engine plays this message
        seconds_total = speech.play_message(message)
        time.sleep(seconds_total + 1)

        speech_queue.task_done()



def should_play_message():
    """Check if 10 seconds have passed since the last error message."""
    global last_error_time
    current_time = time.time()
    if current_time - last_error_time >= ERROR_DELAY:
        last_error_time = current_time
        return True
    return False

def video_frame_callback(frame: av.VideoFrame, selected_exercise, user_name, st=None):
    """Callback to process each video frame and run the selected model."""
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
        detection = exercise_model.detect(mp_results=results, image=image, timestamp=frame.time, user_name=user_name)

        if selected_exercise == "Plank":
            predicted_class = detection.get("predicted_class", "")
            if predicted_class == "L" and should_play_message():
                print("I WANT TO SPEAK, LET ME SPEAK. ")
                speech_queue.put("Lower back")
            elif predicted_class == "H" and should_play_message():
                speech_queue.put("Higher back")

        elif selected_exercise == "Bicep Curl":
            predicted_class = detection.get("predicted_class", "")
            if predicted_class != "C" and should_play_message():
                speech_queue.put("Error")

        elif selected_exercise == "Squat":
            feet_placement = detection.get("squat_details", {}).get("feet_placement", None)
            knee_placement = detection.get("squat_details", {}).get("knee_placement", None)
            if feet_placement == "too tight" and should_play_message():
                speech_queue.put("feet too tight")
            elif feet_placement == "too wide" and should_play_message():
                speech_queue.put("feet too wide")
            elif knee_placement == "too tight" and should_play_message():
                speech_queue.put("knee too tight")
            elif knee_placement == "too wide" and should_play_message():
                speech_queue.put("knee too wide")

        elif selected_exercise == "Lunge":
            knee_error = detection.get("knee_over_toe_error", {}).get("status", None)
            if knee_error == "Incorrect" and should_play_message():
                speech_queue.put("knees are over toe")

            # Start speech playback in a separate thread if there are new messages
        if not speech_queue.empty():
            threading.Thread(target=play_message_in_background, args=(speech_queue,)).start()

    return av.VideoFrame.from_ndarray(image, format="bgr24")


def video_stream(choice , user_name):
    webrtc_streamer(
        key="posture-correction",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_frame_callback=lambda frame: video_frame_callback(frame, choice, user_name),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

