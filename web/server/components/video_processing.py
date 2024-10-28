import cv2
import mediapipe as mp
from detection_realtime.plank import PlankDetection
from detection_realtime.bicep_curl import BicepCurlDetection
from detection_realtime.squat import SquatDetection
from detection_realtime.lunge import LungeDetection
import base64
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode

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
exercise_data_collection = []  # This will collect data across frames


def extract_landmarks(landmarks):
    """Extract landmarks into a list."""
    if landmarks is not None:
        return [(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks.landmark]
    return []  # Return empty list if no landmarks


def video_frame_callback(frame: av.VideoFrame, selected_exercise):
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
        detection = exercise_model.detect(mp_results=results, image=image, timestamp=frame.time)

        # Collect data from detection
        # Convert the image to base64 to pass it as a string
        _, buffer = cv2.imencode('.jpg', image)  # Encode the image to JPEG format
        # frame_data = base64.b64encode(buffer).decode('utf-8')  # Encode as base64 string

        # Extract landmarks
        landmarks_data = extract_landmarks(results.pose_landmarks)

        # Prepare data to collect
        data_to_collect = {
            "timestamp": frame.time,
            "exercise": selected_exercise,
            "detection_results": detection,  # or any specific results from your detection
            "landmarks": landmarks_data,  # Store the landmarks data
            # "frame": frame_data  # Store the base64-encoded frame if needed
        }
        exercise_data_collection.append(data_to_collect)  # Append collected data

    return av.VideoFrame.from_ndarray(image, format="bgr24")


def video_stream(choice):
    webrtc_streamer(
        key="posture-correction",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_frame_callback=lambda frame: video_frame_callback(frame, choice),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=False,
    )

    return exercise_data_collection  # Return the collected data
