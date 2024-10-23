import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'  # Replace with your actual OpenAI API key

# Streamlit app interface
st.title("ChatGPT Integration with Streamlit")

# Input field for user query
user_input = st.text_input("Enter your query for ChatGPT:")

# Button to send the query
if st.button("Send to ChatGPT"):
    if user_input:
        try:
            # Call the OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",  # You can replace with other GPT models
                prompt=user_input,
                max_tokens=100  # You can adjust this value based on how much output you want
            )

            # Display the response from ChatGPT
            st.subheader("ChatGPT Response:")
            st.write(response['choices'][0]['text'].strip())

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query to send to ChatGPT.")
