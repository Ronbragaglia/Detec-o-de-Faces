# -*- coding: utf-8 -*-
"""detecção face Goku

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LZTdXGe8F2vsnQ3kWAwMKbEla9WrhPvK
"""

!pip install deepface

import deepface
print(deepface.__version__)

import cv2
import numpy as np
from deepface import DeepFace
import requests
from io import BytesIO
from PIL import Image
from google.colab.patches import cv2_imshow

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print("Erro ao baixar a imagem:", e)
        return None

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return faces, image

def classify_faces(image, faces):
    classifications = []

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        prediction = DeepFace.analyze(face, actions=['age', 'gender', 'race', 'emotion'])
        classifications.append(prediction)

    return classifications

image_url = "https://wallpapersmug.com/download/1024x768/01e666/Ultra-Instinct-Dragon_Ball-goku.jpg"

image = load_image_from_url(image_url)

if image is not None:
    faces, image_with_faces = detect_faces(image)

    num_faces = len(faces)
    print(f"Número de faces detectadas: {num_faces}")

    classifications = classify_faces(image_with_faces, faces)

    for idx, classification in enumerate(classifications):
        print(f"\nFace {idx+1}:")
        print(f"  Idade: {classification['age']}")
        print(f"  Gênero: {classification['gender']}")
        print(f"  Raça: {classification['dominant_race']}")
        print(f"  Emoção: {classification['dominant_emotion']}")

    cv2_imshow(image_with_faces)
else:
    print("Não foi possível carregar a imagem.")