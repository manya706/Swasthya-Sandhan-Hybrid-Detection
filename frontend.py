import streamlit as st
import base64
from tensorflow import keras
import pennylane as qml
import numpy as np
import cv2
import joblib
from PIL import Image
from pennylane.templates import RandomLayers
# st.title('Detecting Diabetic Retinopathy using Quantum Computing')
st.markdown('<h1 style="color:black;">Detecting Diabetic Retinopathy using Quantum Computing</h1>', unsafe_allow_html=True)

upload= st.file_uploader('Insert image for classification', type=['png','jpg'])

##################################################
# quantum preprocessing
n_layers = 4
dev = qml.device("default.qubit", wires=4)
# Random circuit parameters
rand_params = np.random.uniform(high=2 * np.pi, size=(n_layers, 4))

@qml.qnode(dev, interface="autograd")
def circuit(phi):
    # Encoding of 4 classical input values
    for j in range(4):
        qml.RY(np.pi * phi[j], wires=j)

    # Random quantum circuit
    RandomLayers(rand_params, wires=list(range(4)))

    # Measurement producing 4 classical output values
    return [qml.expval(qml.PauliZ(j)) for j in range(4)]

def quanv(image):
    """Convolves the input image with many applications of the same quantum circuit."""
    out = np.zeros((14, 14, 4))

     # Loop over the coordinates of the top-left pixel of 2X2 squares
    for j in range(0, 28, 2):
        for k in range(0, 28, 2):
            # Process a squared 2x2 region of the image with a quantum circuit
            q_results = circuit(
                [
                    image[j, k, 0],
                    image[j, k + 1, 0],
                    image[j + 1, k, 0],
                    image[j + 1, k + 1, 0]
                ]
            )
            # Assign expectation values to different channels of the output pixel (j/2, k/2)
            for c in range(4):
                out[j // 2, k // 2, c] = q_results[c]
    return out

####################################################

c1, c2= st.columns(2)
if upload is not None:
  im= Image.open(upload)
  img= np.asarray(im)
  image= cv2.resize(img,(256, 256))
  normalized_img = image / 255.0
  img= quanv(normalized_img)
  flattened_img = img.reshape(-1)
#   img= np.expand_dims(img, 0)
  c1.header('Input Image')
  c1.image(im)
  c1.write(img.shape)

  model1 = keras.models.load_model('saved_model.h5')
  model2 = keras.models.load_model('saved_model3.h5')
  ensemble = joblib.load('ensemble_model.joblib')

  predictions_1 = model1.predict(np.expand_dims(img, axis=0))
  predictions_2 = model2.predict(np.expand_dims(img, axis=0))
  c2.write(predictions_1)
  c2.write(predictions_2)

  combined_test_predictions = np.concatenate(
    (predictions_1,predictions_2),
    axis=1
    )
  # Use the ensemble model for prediction
  chain_predictions = ensemble.predict(combined_test_predictions)

    # Calculate probabilities based on chain_predictions for each class
  class_labels = ['Healthy', 'Moderate', 'Mild', 'Proliferate', 'Severe']
  class_probabilities = chain_predictions[0] * 100

    # Display results using Streamlit
  c2.header('Output')
  c2.subheader('Predicted class:')
  predicted_class_idx = np.argmax(chain_predictions)
  predicted_class_label = class_labels[predicted_class_idx]
  c2.write(predicted_class_label)

  c2.subheader('Class Probabilities:')
  for label, prob in zip(class_labels, class_probabilities):
      c2.write(f"{label}: {prob:.2f}%")
#   chain_predictions = ensemble.predict(combined_test_predictions)
# # Predict using the loaded model
# #   pred = model2.predict(np.expand_dims(flattened_img, axis=0))

#   c2.header('Output')
#   output_class = {
#     'Healthy': 0,
#     'Moderate': 1,
#     'Mild': 2,
#     'Proliferate': 3,
#     'Severe': 4,
#     }   
   
#   probability_non_diabetic = chain_predictions[0][0] * 100
#   probability_diabetic = (1 - chain_predictions[0][0]) * 100
# #   c2.write(f"Chances of patient being Diabetic: {probability_diabetic:.2f}%")
# #   c2.write(f"Chances of patient being Not Diabetic: {probability_non_diabetic:.2f}%")
#   c2.subheader('Predicted class :')
#   c2.write(chain_predictions)