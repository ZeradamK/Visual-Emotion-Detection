from flask import Flask, request, jsonify, render_template
import cv2
import base64
import numpy as np
from deepface import DeepFace
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    image_data = data['image']
    image_data = image_data.split(",")[1]
    img_data = base64.b64decode(image_data)
    np_img = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = random.choice(faces)
        face_img = img[y:y + h, x:x + w]

        result = DeepFace.analyze(face_img, actions=['emotion'])
        
        if isinstance(result, list):
            result = result[0]
        return jsonify({'emotion': result['dominant_emotion']})
    else:
        return jsonify({'error': 'No face detected'})


if __name__ == '__main__':
    app.run(debug=True)
