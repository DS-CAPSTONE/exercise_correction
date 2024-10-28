import streamlit as st
import sys
import os
import random
import pymongo
from components import constants, survery, speech, login, video_processing, llm, pain_image
import base64

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# MongoDB setup
uri = constants.db_uri
client = pymongo.MongoClient(uri)
db = client[constants.db_client]  # Your database name
collection = db[constants.db_collection]  # Your collection name


st.session_state['userdata'] = {
    'login username' : '',
    'video_data' : [],
    'pain data' : [],
    'survey data' : [],
}

# Motivational messages
motivational_messages = constants.motivational_messages


def set_page_styles():
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

def display_titles():
    st.title("Real-Time Exercise Posture Correction App")
    st.sidebar.title("Exercise Detection Models")

def login_user():
    login.login()
    st.write("Please log in to continue.")

def welcome_user():
    st.write(f"Hello, {st.session_state['user_name']}! Start your exercise session.")
    
    st.session_state['userdata']["login username"] = st.session_state['user_name']
    
    motivation = random.choice(motivational_messages)
    welcome_message = f"Welcome, {st.session_state['user_name']}!, {motivation}"

    # Convert to speech
    speech.play_message(welcome_message)

def sidebar_options():
    # Chat with AI Trainer
    st.sidebar.title("Chat with AI TRAINER")
    user_input = st.sidebar.text_area("Ask a question:", placeholder="Type here...", key="chat_input")

    if st.sidebar.button("Get Response", key="chat_button"):
        response = llm.gpt_response(user_input)
        
        st.session_state['userdata']["llm data"].append({
            "question":  user_input,
            "response": response,
        })
        
        st.sidebar.write(response)
        # llm.speak_response(response)

def handle_main_content():
    # Add a unique key to avoid duplicate widget ID conflict
    choice = st.sidebar.selectbox("Select Exercise", list(video_processing.exercise_models.keys()), key="main_content_selectbox")

    if choice == "Home":
        display_home_screen()
    else:
        display_webcam_feed(choice)
        display_pain_detection()


def display_home_screen():
    st.write("Welcome to the Exercise Posture Correction App.")
    st.write("""
                This app will help you correct your posture in real-time.
                Choose an exercise model from the sidebar.
            """)

def display_webcam_feed(choice):
    st.header("Webcam Live Feed")
    st.write("Click on start to use the webcam and check for posture correction.")
    video_data =  video_processing.video_stream(choice)
    if video_data:
        st.session_state['userdata']['video_data'] = video_data


def display_pain_detection():
    st.header("Pain Detection System")
    st.write("Click on the skeleton image to indicate pain areas during exercise.")
    recommended_exercise , part , canvas_data = pain_image.handle_image_clicks()
    
    st.session_state['userdata']["pain data"].append(
        {
            "pain area": canvas_data,
            "recommended exercise": recommended_exercise,
            "part": part
        }
    )
    st.write(f"Recommended exercise for paining {part}: {recommended_exercise}")


def get_user_history(username):
    """Fetch user history from the database."""
    user_data = collection.find_one({"login username": username})
    if user_data and 'survey data' in user_data:
        return user_data['survey data']
    return []


def display_user_history():
    """Display the user's historical data."""
    username = st.session_state['userdata']['login username']
    history = get_user_history(username)

    if history:
        st.header("Your Exercise History")
        for entry in history:
            st.write(f"### Date: {entry.get('next_workout_date', 'N/A')}")
            st.write(f"**Weight Recorded:** {entry.get('weight', 'N/A')} kg")
            st.write(f"**Max Heart Rate Recorded:** {entry.get('heart_rate', 'N/A')} bpm")
            st.write(f"**Body Parts Focused:** {', '.join(entry.get('body_parts', []))}")
            st.write(f"**Feelings after Exercise:** {entry.get('feelings', 'N/A')}")
            st.write(f"**Muscle Workout Intensity:** {entry.get('intensity', 'N/A')}")
            st.write(f"**Feelings about the Exercise:** {entry.get('exercise_feeling', 'N/A')}")
            st.write(f"**Pain Description:** {entry.get('pain', 'N/A')}")
            if 'workout_image' in entry:
                st.image(base64.b64decode(entry['workout_image']), caption="Workout Image", use_column_width=True)
            st.write("---")
    else:
        st.write("No history found for this user.")

def main():
    set_page_styles()
    display_titles()
    
    # Check if user is logged in
    if "user_name" in st.session_state:
        welcome_user()
        sidebar_options()
        handle_main_content()
        display_user_history()
        survey_data = survery.survey_section() 
        if survey_data:
            st.session_state['userdata']["survey data"].append(survey_data)
            collection.insert_one(st.session_state['userdata'])
            st.write("Thank you for completing the survey.")
    else:
        login_user()
    

if __name__ == "__main__":
    main()
