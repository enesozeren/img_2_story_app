import requests
import os
from dotenv import load_dotenv
from transformers import pipeline

# Get the huggingface token from env
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
ELEVENLABS_API_TOKEN = os.getenv("ELEVENLABS_API_TOKEN")

# Get the serverless inference api from huggingface
I2TM_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
LLM_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
T2SM_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/repzAAjoKlgcT2oOAIWt"


def image_2_text(image_filename):

    with open(image_filename, "rb") as f:
        data = f.read()

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(I2TM_API_URL, headers=headers, data=data)
    
    return response.json()[0]["generated_text"]


def generate_story(caption):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": f"Create a short story that contains 50 words about {caption}:",
        "parameters": {
            "return_full_text": False,
            "max_new_tokens": 100
        }
    }

    story = requests.post(LLM_API_URL, headers=headers, json=payload)

    return story.json()[0]["generated_text"]


def text_2_speech(story):
    CHUNK_SIZE = 1024
    
    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_TOKEN
    }

    data = {
    "text": story,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(T2SM_API_URL, json=data, headers=headers)
    with open('story_audio.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)