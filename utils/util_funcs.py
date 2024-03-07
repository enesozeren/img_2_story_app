import requests
import streamlit as st

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Get the serverless inference api from huggingface
I2TM_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
LLM_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
T2SM_API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"


def image_2_text(image_filename):
    with open(image_filename, "rb") as f:
        data = f.read()    
    response = requests.post(I2TM_API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]


def generate_story(caption):
    payload = {
        "inputs": f"Create a short very funny story that contains 50 words about {caption}:",
        "parameters": {
            "return_full_text": False,
            "max_new_tokens": 100
        }
    }
    story = requests.post(LLM_API_URL, headers=headers, json=payload)
    return story.json()[0]["generated_text"]


def text_2_speech(story):
    payload = {
        "inputs": story
    }
    response = requests.post(T2SM_API_URL, headers=headers, json=payload)
    with open('story_audio.mp3', 'wb') as f:
        f.write(response.content)