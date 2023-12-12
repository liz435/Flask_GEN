import streamlit as st
import requests
import io
from PIL import Image
import cv2


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

GEN_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

FER_API_URL = "https://api-inference.huggingface.co/models/RickyIG/emotion_face_image_classification_v3"

headers = {"Authorization": "Bearer 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"}

def fer(filename):
    data = filename
    response = requests.post(FER_API_URL, headers=headers, data=data)
    return response.json()



headers = {"Authorization": "Bearer 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"}

# App title and header
st.title("My Streamlit App")
st.header("This is a simple Streamlit app template")

def describ(filename):
    data = filename
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


def generate(payload):
	response = requests.post(GEN_API_URL, headers=headers, json=payload)
	return response.content



picture = st.camera_input("Take a picture")

if picture:
    image_bytes = None
    st.image(picture)
    emotion = fer(picture)
    if emotion:
        st.write(emotion[0][0])
    caption = describ(picture)
    if caption:
        st.write(caption[0]['generated_text'])
        image_bytes = generate({
        "inputs":"a cute cat",
    })
        img_buffer = io.BytesIO(image_bytes)
        gen_image = Image.open(img_buffer)
        st.image(gen_image)
