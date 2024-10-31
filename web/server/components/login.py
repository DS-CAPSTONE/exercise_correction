import streamlit as st


def login():
    if "user_name" not in st.session_state:
        # Sidebar login section
        with st.sidebar:
            st.markdown("### Please log in to continue.")
            user_name = st.text_input("Enter your name:", key="user_name_input")
            login_button = st.button("Login")

            if login_button and user_name:
                # Store the user name in session state
                st.session_state["user_name"] = user_name
                
                # Rerun the app to reflect the login
                st.rerun()

            elif login_button and not user_name:
                st.error("Please enter your name to log in.")
   