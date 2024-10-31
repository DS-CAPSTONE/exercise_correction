import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from detection_realtime.utils import ( get_static_file_url )
from components import constants
skeleton_img = get_static_file_url("assets/skeleton.jpg")
import random
exercise_recommendations = constants.exercise_recommendations

body_parts = constants.body_parts


# Function to identify body part based on coordinates
def identify_body_part(x, y):
    for part, (x_min, y_min, x_max, y_max) in body_parts.items():
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return part
    return "Unknown"

def handle_image_clicks():
    img = Image.open(skeleton_img)
    
    # Canvas for detecting clicks
    canvas_result = st_canvas(
        background_image=img,
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=0,
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="point",
        key="pain_canvas"
    )

    if "coordinates" not in st.session_state:
        st.session_state["coordinates"] = (None, None)

    if canvas_result.json_data is not None:
        for obj in canvas_result.json_data["objects"]:
            x, y = obj["left"], obj["top"]
            st.session_state["coordinates"] = (x, y)

    if st.session_state["coordinates"] != (None, None):
        x, y = st.session_state["coordinates"]
        part = identify_body_part(x, y)
        st.write(f"Latest Clicked Point - x: {x}, y: {y}, part: {part}")

        recommended_exercise = random.choice(
            exercise_recommendations.get(part, ["No exercise recommendation available for this body part."])
        )
        
        return recommended_exercise , part , canvas_result.json_data
    
    return None, None, None