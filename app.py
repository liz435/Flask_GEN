from flask import Flask, render_template, request, url_for, redirect, jsonify

import requests
import cv2
import io
from PIL import Image


app = Flask(__name__)


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}


def textToImage(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    with open("static/generated_image.jpg", "wb") as f:
        f.write(response.content)
    return "static/generated_image.jpg"




def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def capture_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        raise Exception("Error opening webcam")
    # Capture a frame
    ret, frame = cap.read()
    # Check if the frame is captured successfully
    if not ret:
        raise Exception("Error capturing image")
    # Release the webcam
    cap.release()
    # Save the captured frame as an image
    cv2.imwrite("captured_image.jpg", frame)
    cv2.imwrite("static/captured_image.jpg", frame)
    return "captured_image.jpg"


@app.route('/', methods=['GET', 'POST'])
def home():
    filename = None
    caption = None
    
    if request.method == "POST":
        filename = capture_image()
        caption = query(filename)
        print(caption)

        image = textToImage({
        "inputs": 'Astronaut riding a horse',
    })



    return render_template('index.html', filename=filename, caption=caption, image =image)

if __name__ == '__main__':
    print('running this cell')
    app.run(debug=True, host='0.0.0.0', port=5001)