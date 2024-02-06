from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from pydantic import BaseModel
from tensorflow import keras, stack
from tensorflow.io import decode_image
from tensorflow import image
import time
from numpy import argmax, amax
import csv
import base64

app = FastAPI()
# pre-load the model so everything is just faster.
model = keras.models.load_model("./models/BEST-cnn.keras")
labellist = ['Acne, or Rosacea', 'Actinic Keratosis, or other Malignant Lesions', 
            'Alopecia, or other Hair Diseases', 'Atopic Dermatitis', 'Bacterial Infections', 
            'Benign Tumors', 'Bullous Disease', 'Connective Tissue Diseases', 'Eczema', 
            'Exanthems, or Drug Eruptions', 'Fungal Infections', 'Healthy or Benign growth', 
            'Herpes, HPV, other STDs', 'Lyme Diseasem, Infestations and Bites', 
            'Melanoma Skin Cancer Nevi and Moles', 'Nail Fungus or other Nail Disease', 
            'Poison Ivy or Contact Dermatitis', 'Psoriasis, Lichen Planus or related diseases', 
            'Systemic Disease', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 
            'Warts, or other Viral Infections']


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")    # defining the root directory
async def root():
    return {"message": "hello world manya"}

name1 = "SIH 2023"
@app.get("/greet/{name}")
async def name(name: str = name1):
    return {"message": f"welcome to {name}"}

@app.get("/health")    # just to check if the api is working
def check_health():
    return {"status": "API is working!!"}

# main project logic -------->
class ImageInput(BaseModel):
    images: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]
    pincode: str

def write_to_csv(prediction, ttime, pincode, confidence):
    with open('./Backend/predictions.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ttime, pincode, prediction, confidence])

# make a little function here to postprocess the model's output
# LABEL and FORMAT tensors correctly :)
def postprocess(pred, labellist=labellist, weight=0.85):
    arg = argmax(pred, axis=1)[0]
    conf_arr = amax(pred, axis=1)
    try:
        confidence = conf_arr[0]*weight + conf_arr[1]*(1 - weight)
    except:
        confidence = conf_arr[0]
    label = labellist[arg]
    final_pred = {'label' : label, 'confidence' : (confidence * (1 // confidence))*100}

    # write_to_csv(final_pred, request.pincode) 
    return final_pred

@app.post("/predict/")
async def predict_images(request: ImageInput):
    processed_images = []
    starttime = time.time() # stopwatch start
    
    for img in request.images:
        # Read the JSON image data
        json_image_data = await img.read()
        # Decode the image from JSON data, and resize
        image_tensor = decode_image(json_image_data, channels=3)  # Set the number of color channels (3 for RGB)
        resized_image = image.resize(image_tensor, size=(256, 256))
        # Append the processed image to the list
        processed_images.append(resized_image)

    # Convert the list of processed images to a TensorFlow tensor
    images_tensor = stack(processed_images)
    # get prediction from the model
    prediction = model.predict(images_tensor)
    endtime = time.time() # stopwatch stop
    ttime = endtime - starttime
    # replace this with a more elaborate argmax function
    final_pred = postprocess(prediction)
    write_to_csv(final_pred['label'], ttime, request.pincode, final_pred['confidence'])

    return {"prediction" : final_pred, 'exectime' : ttime}

@app.post("/form-predict/")
async def form_predict(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")],
    pincode: Annotated[str, Form()]
    ):
    processed_images = []
    starttime = time.time() # stopwatch start
    
    for img in files:
        # Read the JSON image data
        json_image_data = await img.read()
        # Decode the image from JSON data, and resize
        image_tensor = decode_image(json_image_data, channels=3)  # Set the number of color channels (3 for RGB)
        resized_image = image.resize(image_tensor, size=(256, 256))
        # Append the processed image to the list
        processed_images.append(resized_image)

    # Convert the list of processed images to a TensorFlow tensor
    images_tensor = stack(processed_images)
    # get prediction from the model
    prediction = model.predict(images_tensor)
    
    endtime = time.time() # stopwatch stop
    
    ttime = endtime - starttime
    # replace this with a more elaborate argmax function
    final_pred = postprocess(prediction)
    write_to_csv(final_pred['label'], ttime, pincode, final_pred['confidence'])
    y_pred = {"prediction" : final_pred, 'exectime' : ttime}
    print(y_pred)
    return y_pred

if __name__ == '__main__':
    # CODE FOR SERVER
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)