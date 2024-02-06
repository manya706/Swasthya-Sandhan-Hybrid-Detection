from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import base64
from tensorflow import keras
import pennylane as qml
import numpy as np
import cv2
import joblib
from PIL import Image
from pennylane.templates import RandomLayers
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Quantum preprocessing
n_layers = 4
dev = qml.device("default.qubit", wires=4)
rand_params = np.random.uniform(high=2 * np.pi, size=(n_layers, 4))
def quanv(image):
    out = np.zeros((14, 14, 4))
    for j in range(0, 28, 2):
        for k in range(0, 28, 2):
            q_results = circuit([
                image[j, k, 0],
                image[j, k + 1, 0],
                image[j + 1, k, 0],
                image[j + 1, k + 1, 0]
            ])
            for c in range(4):
                out[j // 2, k // 2, c] = q_results[c]
    return out

@qml.qnode(dev, interface="autograd")
def circuit(phi):
    for j in range(4):
        qml.RY(np.pi * phi[j], wires=j)
    RandomLayers(rand_params, wires=list(range(4)))
    return [qml.expval(qml.PauliZ(j)) for j in range(4)]
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        img_array = np.asarray(img)
        image = cv2.resize(img_array, (256, 256)) / 255.0
        processed_image = quanv(image)

        model1 = keras.models.load_model('saved_model.h5')
        model2 = keras.models.load_model('saved_model3.h5')
        ensemble = joblib.load('ensemble_model.joblib')

        predictions_1 = model1.predict(np.expand_dims(processed_image, axis=0))
        predictions_2 = model2.predict(np.expand_dims(processed_image, axis=0))

        combined_test_predictions = np.concatenate((predictions_1, predictions_2), axis=1)
        chain_predictions = ensemble.predict(combined_test_predictions)

        class_labels = ['Healthy', 'Moderate', 'Mild', 'Proliferate', 'Severe']
        class_probabilities = predictions_2[0] * 100

        predicted_class_idx = np.argmax(predictions_2)
        predicted_class_label = class_labels[predicted_class_idx]

        return {
            "message": "Image uploaded and processed successfully",
            "predicted_class": predicted_class_label,
            "class_probabilities": {label: prob.item() for label, prob in zip(class_labels, class_probabilities)},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)

async def read_item():
    with open("templates/DR-detection.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

