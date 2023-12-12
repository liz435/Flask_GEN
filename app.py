from flask import Flask, render_template, request, send_file
from io import BytesIO

import requests
import cv2
from PIL import Image
import io
import time

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
API_URL2 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {"Authorization": "Bearer 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"}

# def serve_pil_image(pil_img):
#     img_io = BytesIO()
#     pil_img.save(img_io, 'JPEG', quality=70)
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/jpeg')

def text_to_image(payload):
    response = requests.post(API_URL2, headers=headers, json=payload)
    print(type(response.content))
    return response.content


def describtion(filename):
    with open("static/" + filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def capture_image():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
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
    image = None
    image_buffer = None
    image_name = None

    
    if request.method == "POST":
        filename = capture_image()
        caption = describtion(filename)

        if caption:
            image_bytes = text_to_image({
                "inputs" : caption[0]['generated_text'],
            })
            try:
                print(image_bytes)
                image_buffer = io.BytesIO(image_bytes)
                image = Image.open(image_buffer)
                image.save("static/output.jpg", format="JPEG")
            except Exception as e:
                print(f"Unexpected error: {e}")
                
    return render_template('index.html', filename=filename, caption=caption, image=image)

if __name__ == '__main__':
    print('running this cell')
    app.run(debug=True, host='0.0.0.0', port=5001)
