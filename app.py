import requests
import os
from dotenv import load_dotenv

# Get the huggingface token from env
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
ELEVENLABS_API_TOKEN = os.getenv("ELEVENLABS_API_TOKEN")
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Get the serverless inference api from huggingface
LLM_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
I2TM_API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
T2SM_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/repzAAjoKlgcT2oOAIWt"

def image_2_text(image_filename):
    with open(image_filename, "rb") as f:
        data = f.read()
    response = requests.post(I2TM_API_URL, headers=headers, data=data)
    return response.json()

caption = image_2_text("savunmadım.jpg")
print(caption)

def generate_story(payload):
	response = requests.post(LLM_API_URL, headers=headers, json=payload)
	return response.json()
	
story = generate_story({
	"inputs": 
	f"""
	The machine takes a text input and returns a funny story from the input.
	INPUT: {caption}
	MACHINE OUTPUT:
	"""
})

print(story[0]["generated_text"])

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
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

text_2_speech(story[0]["generated_text"])          