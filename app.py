# @title
import requests
import io
from PIL import Image
from IPython.display import display
import time

#API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
# API_URL = "https://api-inference.huggingface.co/models/Kvikontent/midjourney-v6"
#API_URL = "https://api-inference.huggingface.co/models/Yntec/dreamlike-photoreal-remix"
headers = {"Authorization": "Bearer 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"}  # Replace 'hf_token' with your actual Hugging Face token

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 503 and "loading" in response.text:
        return None
    else:
        raise Exception(f"Failed to generate image: {response.status_code} - {response.text}")

def generate_image(prompt, max_retries=10, wait_time=5):
    payload = {"inputs": prompt}
    for attempt in range(max_retries):
        image_bytes = query(payload)
        if image_bytes:
            return image_bytes
        else:
            print(f"Model is loading. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    raise Exception("Failed to generate image after multiple attempts.")

try:
    image_bytes = generate_image("A high-resolution, photorealistic image of an Indian brahman dog standing in a grassy field with mountains in the background")

    # Open the image with PIL and display it
    image = Image.open(io.BytesIO(image_bytes))
    display(image)
except Exception as e:
    print(e)
