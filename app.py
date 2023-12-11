from flask import Flask, render_template, request, send_file
from io import BytesIO

import requests
import cv2
import os
from PIL import Image
import io

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

# def serve_pil_image(pil_img):
#     img_io = BytesIO()
#     pil_img.save(img_io, 'JPEG', quality=70)
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/jpeg')

def text_to_image(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


def query(filename):
    with open("static/" + filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Error opening webcam")
    ret, frame = cap.read()
    if not ret:
        raise Exception("Error capturing image")
    cap.release()

    filename = "captured_image.jpg"
    cv2.imwrite("static/" + filename, frame)
    return filename

@app.route('/', methods=['GET', 'POST'])
def home():
    filename = None
    caption = None
    image_bytes = None
    image = None
    
    if request.method == "POST":
        filename = capture_image()
        caption = query(filename)

        if caption:

            image_bytes = text_to_image({
                "inputs" : "cat sitting on a rock",
            })
            print(image_bytes)
            print('imhere')

            # image = Image.open(io.BytesIO(image_bytes))

    return render_template('index.html', filename=filename, caption=caption[0]['generated_text'], image=image)

if __name__ == '__main__':
    print('running this cell')
    app.run(debug=True, host='0.0.0.0', port=5001)
