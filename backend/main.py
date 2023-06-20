import logging
import threading
import os

import schedule
import torch
import uvicorn
from app.weather_api import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.events import router
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from vision.detection import models
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.DEBUG)
device=torch.device("cpu")
relative_path = './vision/detection/best_model_mobilenet_singleclass.pt'
absolute_path = os.path.abspath(relative_path)
model = torch.load(absolute_path,
                   map_location=device)
# model = models.build_model(backbone="mobile", num_classes=2)
# model.load_state_dict(
#     torch.load("backend/vision/detection/best_model(mobilenet,single class).pt",
#                 map_location=device))

app = FastAPI()
app.add_middleware(
    SessionMiddleware, 
    secret_key="BigForest5050", 
    max_age=3600
    )
#모든 url접근허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)



app.include_router(router)
app.mount("/storage", StaticFiles(directory="/home/ubuntu/withskin/backend/storage/"), name="storage")

weather_data={
            'uv': None, 
            'temperature':None, 
            'humidity': None,
            'pm10' : None,
            'pm2_5' : None
            }
for _ in range(128):
    try:
        weather_data = update_weather_data()
        print(weather_data)
        print("성공")
        time.sleep(20)
        break
    except:
        time.sleep(10)
        print("날씨 api 실패")
        pass
# try:
#     schedule.every().hour.at(':16').do(update_weather_data)
#     t = threading.Thread(target=run_schedule)
#     t.start()

# except:
#     print("갱신 실패")
#     pass


@app.get("/api/weather")
async def get_weather():
    try:
        new_weather_data=update_weather_data()
        print(weather_data)

    
        response = JSONResponse(content={'weather_data': new_weather_data})
        response.headers['Cache-Control'] = 'no-store, no-store, must-revalidate'
        response.headers['Pragma'] ="no-cache"
        response.headers["Expires"] = "0"
        return response
    except:
        response = JSONResponse(content={'weather_data': weather_data})
        response.headers['Cache-Control'] = 'no-store, no-store, must-revalidate'
        response.headers['Pragma'] ="no-cache"
        response.headers["Expires"] = "0"
        return response



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
