import mediapipe as mp
import cv2
import numpy as np
import datetime
import os
import math
from django.conf import settings

# Drawing helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# * Mediapipe Utils Functions
def calculate_angle(point1: list, point2: list, point3: list) -> float:
    """Calculate the angle between 3 points

    Args:
        point1 (list): Point 1 coordinate
        point2 (list): Point 2 coordinate
        point3 (list): Point 3 coordinate

    Returns:
        float: angle in degree
    """
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)
    # print("Point 1: ", point1, "Point 2: ", point2, "Point 3: ", point3)

    # Calculate algo

    vector1 = point1 - point2
    vector2 = point3 - point2

    dot_product = np.dot(vector1, vector2)

    cross_product = np.linalg.norm(np.cross(vector1, vector2))

    angleInRad = np.arctan2(cross_product, dot_product)
    # print("Angle in radian: ", angleInRad)

    angleInDeg = np.degrees(angleInRad)
    # print("Angle in degree: ", angleInDeg)

    return angleInDeg



def calculate_distance(pointX: list, pointY: list) -> float:
    """Calculate distance between 2 points in a frame

    Args:
        pointX (list): First point coordinate
        pointY (list): Second point coordinate

    Returns:
        float: _description_
    """

    x1, y1, z1 = pointX
    x2, y2, z2 = pointY

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def extract_important_keypoints(results, important_landmarks: list) -> list:
    """Extract important landmarks' data from MediaPipe output

    Args:
        results : MediaPipe Pose output
        important_landmarks (list): list of important landmarks

    Returns:
        list: list of important landmarks' data from MediaPipe output
    """
    landmarks = results.pose_landmarks.landmark

    data = []
    for lm in important_landmarks:
        keypoint = landmarks[mp_pose.PoseLandmark[lm].value]
        data.append([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility])

    return np.array(data).flatten().tolist()


def get_drawing_color(error: bool) -> tuple:
    """Get drawing color for MediaPipe Pose

    Args:
        error (bool): True if correct pose, False if incorrect pose

    Returns:
        tuple: RGB colors
    """
    LIGHT_BLUE = (244, 117, 66)
    LIGHT_PINK = (245, 66, 230)

    LIGHT_RED = (29, 62, 199)
    LIGHT_YELLOW = (1, 143, 241)

    return (LIGHT_YELLOW, LIGHT_RED) if error else (LIGHT_BLUE, LIGHT_PINK)


# * OpenCV util functions
def rescale_frame(frame, percent=50):
    """Rescale a frame from OpenCV to a certain percentage compare to its original frame

    Args:
        frame: OpenCV frame
        percent (int, optional): percent to resize an old frame. Defaults to 50.

    Returns:
        _type_: OpenCV frame
    """
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def save_frame_as_image(frame, message: str = None):
    """
    Save a frame as image to display the error
    """
    now = datetime.datetime.now()

    if message:
        cv2.putText(
            frame,
            message,
            (50, 150),
            cv2.FONT_HERSHEY_COMPLEX,
            0.4,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

    print("Saving ...")
    cv2.imwrite(f"../data/logs/bicep_{now}.jpg", frame)


# * Other util functions
def get_static_file_url(file_name: str) -> str:
    """Return static url of a file

    Args:
        file_name (str)

    Returns:
        str: Full absolute path of the file. Return None if file is not found
    """

    path = f"/Users/jainilpatel/PycharmProjects/Exercise-Correction/web/server/static/{file_name}"


    return path if os.path.exists(path) else None


import streamlit as st
import sys
import os
import random
import pymongo
from components import constants, survery, speech, login, video_processing, llm, pain_image
import base64

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# Motor setup for asynchronous MongoDB handling
uri = constants.db_uri
client = AsyncIOMotorClient(uri)
db = client[constants.db_client]  # Database name

import asyncio

async def async_insert_dict_to_mongodb(dictionary, user_name):
    """
    Asynchronously insert a dictionary into MongoDB
    """
    dictionary["login username"] = user_name
    dictionary["utc_timestamp"] = datetime.datetime.utcnow()  # Use UTC for consistency
    collection = db[user_name]  # Collection named per user
    await collection.insert_one(dictionary)

async def insert_in_process_async(dictionary, user_name):
    """
    Run async MongoDB insertion without using asyncio.run().
    """
    await async_insert_dict_to_mongodb(dictionary, user_name)


def insert_in_process(dictionary, user_name):
    """
    Insert function compatible with both running and non-running event loops.
    """
    try:
        # Check if there's an active event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None  # No event loop is running

    if loop and loop.is_running():
        # If there is a running loop, create a task
        asyncio.create_task(insert_in_process_async(dictionary, user_name))
    else:
        # Otherwise, use asyncio.run()
        asyncio.run(insert_in_process_async(dictionary, user_name))

# def insert_dicts_to_mongodb_in_parallel(dicts, user_name):
#     """
#     Insert multiple dictionaries in parallel across different cores.
#     """
#     with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
#         futures = [executor.submit(insert_in_process, dictionary, user_name) for dictionary in dicts]


# Function to convert numpy types to native Python types
def convert_numpy_types(data):
    if isinstance(data, dict):
        return {key: convert_numpy_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()  # Convert numpy arrays to lists
    else:
        return data
