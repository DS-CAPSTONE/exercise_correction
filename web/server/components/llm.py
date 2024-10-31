import openai
from components import constants
# Initialize OpenAI API
openai.api_key = constants.openai_api_key
from components import speech
import time
import streamlit as st

def gpt_response(input):
    if input:
        response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": input}],
                max_tokens=100
            )
        return "TRAINER says: " + response['choices'][0]['message']['content'].strip()
    else:
        return "Please type your problem to ger response"
    

def speak_response(response_ai):
    if response_ai:
        seconds_total = speech.play_message(response_ai)
        time.sleep(seconds_total + 1)