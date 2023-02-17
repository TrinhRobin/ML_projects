from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import joblib
import sklearn 
model = joblib.load("model.joblib")

class PredictionItem(BaseModel):
    gender : Optional[int]#0 or 1,
    age: Optional[float]#28.0,
    age_o : Optional[float]#31.0,
    attractive_o: Optional[int]#5,
    sinsere_o: Optional[int]#7,
    funny_o : Optional[int]#1,
    intelligence_o: Optional[int]#0,
    funny_partner : Optional[int]#4,
    attractive_partner : Optional[int]#9,
    sincere_partner: Optional[int]#2,
    intelligence_partner : Optional[int]#4
    shared_interests_important : Optional[int]#3
   

app = FastAPI()

@app.get("/")
def welcome():
    return {"test": "is_running"}

@app.post("/prediction")
def requetage(item: PredictionItem):
    data = load_data(item)
    data = transform_data(data)
    predicted = prediction(data)
    return {"prediction": int(predicted)}

def load_data(data):
    data = pd.DataFrame(pd.Series(data.dict())).T
    return data

def transform_data(data):

    return data

def prediction(data):
    predicted = model.predict(data)
    return predicted