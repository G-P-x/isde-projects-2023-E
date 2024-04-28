import json
from typing import Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis
from rq import Connection, Queue
from rq.job import Job
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.ml.classification_utils import classify_image
from app.utils import list_images
from app.data_storage import result_storage
from fastapi.responses import FileResponse
import json
import matplotlib.pyplot as plt

app = FastAPI()
config = Configuration()
result = result_storage()



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
    result.generate_JSON(classification_score= classification_scores)  #generate JSON file for the result of classification-score
    with open("result.json", "w") as f:
        json.dump(result.classification_results, f)  #write the result into the JSON file   
    data = [classification_scores[0][1], classification_scores[1][1], classification_scores[2][1], classification_scores[3][1], classification_scores[4][1]]
    labels = [classification_scores[0][0], classification_scores[1][0], classification_scores[2][0], classification_scores[3][0], classification_scores[4][0]]
    colors = [(26/255,74/255,4/255,0.8), (117/255,0/255,20/255,0.8), (121/255,87/255,3/255,0.8), (6/255,33/255,108/255,0.8), (63/255,3/255,85/255,0.8)]
    plt.figure(figsize=(15, 10))
    plt.barh(labels, data, color=colors)  
    plt.gca().invert_yaxis()  # Invert the y-axis
    plt.grid(True)
    plt.title('Output Scores', size=20, style='italic', color='black')
    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=16)


    # Save the chart as a PNG file
    plt.savefig('plot.png')
    
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/classifications/result")
async def download_result():
    return FileResponse('result.json', media_type='application/json', filename='result.json')

@app.get("/classifications/plot")
async def download_plot():
    return FileResponse('plot.png', media_type='image/png', filename='plot.png')
    
