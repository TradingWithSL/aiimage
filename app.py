import requests
import io
from PIL import Image
import streamlit as st
import time

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_TOKEN"}  # Replace with your Hugging Face token

# Function to query the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 503 and "loading" in response.text:
        return None
    else:
        raise Exception(f"Failed to generate image: {response.status_code} - {response.text}")

# Function to generate image with retry mechanism
def generate_image(prompt, max_retries=10, wait_time=5):
    payload = {"inputs": prompt}
    for attempt in range(max_retries):
        image_bytes = query(payload)
        if image_bytes:
            return image_bytes
        else:
            st.warning(f"Model is loading. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    raise Exception("Failed to generate image after multiple attempts.")

# Streamlit app
st.title("AI Image Generator")
st.write("Enter a prompt and generate an image using the Stability AI model via Hugging Face API.")

# User input for the prompt
prompt = st.text_input("Enter your prompt", value="A high-resolution, photorealistic image of an Indian brahman dog standing in a grassy field with mountains in the background")

# Button to trigger the image generation
if st.button("Generate Image"):
    try:
        with st.spinner("Generating image... please wait!"):
            image_bytes = generate_image(prompt)

            # Open the image with PIL and display it in Streamlit
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")
