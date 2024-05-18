import json
import cv2
import numpy as np
from typing import Dict, List
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.forms.histogram_form import HistogramForm
import redis
from rq import Connection, Queue
from rq.job import Job
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.ml.classification_utils import classify_image
from app.utils import list_images
from app.ml.image_uploader import upload_image
from app.ml.image_uploader import remove_uploaded_image



app = FastAPI()
config = Configuration()


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> Dict[str, List[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications")
def create_classify(request: Request):
    
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )


@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )
@app.get("/image_histogram")
def create_histogram(request: Request):
         return templates.TemplateResponse(
            "histogram_select.html",
            {"request": request, "images": list_images()},
         )

@app.post("/image_histogram")
async def request_classification(request: Request):
        form = HistogramForm(request)
        await form.load_data()
        image_id = form.image_id

        # read image
        im = cv2.imread('app/static/imagenet_subset/' + image_id)
        # calculate mean value from RGB channels and flatten to 1D array
        vals = im.mean(axis=2).flatten()
        # calculate histogram
        histogram, bins = np.histogram(vals, range(257))

        return templates.TemplateResponse(
            "histogram_output.html",
            {
                "request": request,
                "image_id": image_id,
                "histogram": json.dumps(histogram.tolist()),
            },
        )


    


@app.get("/image_from_PC")  
def select_single_image(request: Request):
    
    # Removing the image to prevent overwriting
    remove_uploaded_image()
    
    return templates.TemplateResponse(
        "classification_select_image.html",
        {"request": request, "models": Configuration.models},
    )


@app.post("/image_from_PC")
async def create_upload_image(request: Request, file: UploadFile = File(...)):
    # Check if the uploaded file is a PNG or JPEG
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PNG or JPEG files are allowed. Try again!")
    contents = await file.read()
    image_id = upload_image(contents)
    form = ClassificationForm(request)
    await form.load_data()
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    
    return templates.TemplateResponse(
        "classification_output_from_upload.html",
        {"request": request,
         "image_id": image_id,
         "classification_scores": json.dumps(classification_scores),
         })
    