from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from model import RainsModelV1, RainsModelV2
import json

users_db = {
    "alice": {
        "username" : "alice",
        "password" : "wonderland"       
    },
    "bob": {
        "username" : "bob",
        "password" : "builder"   
    },
    "clementine": {
        "username" : "clementine",
        "password" : "mandarines" 
    }
}

class V1Item(BaseModel):
    Humidity9am: int
    Humidity3pm: int
    WindGustSpeed: int
    Pressure9am: float
    MaxTemp: float
    Rainfall: float
    WindGustDir: str
    Location: str
    RainToday: str
    Month: int

class V2Item(BaseModel):
    MinTemp: float
    MaxTemp: float
    WindGustSpeed: int
    WindSpeed3pm: int
    Humidity3pm: int
    Pressure9am: float
    Pressure3pm: float
    RainToday: str    
 

security = HTTPBasic()

async def verify_token(credendials : HTTPBasicCredentials = Depends(security)):
    username = credendials.username
    password = credendials.password

    user_dict = users_db.get(username)

    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if user_dict['password'] == password:
        return True
    else:
        raise HTTPException(status_code=401, detail="Incorrect password, unauthorized")


app = FastAPI(title="Rains model api",
                description="API for rains tomorrow prediction in Australia")

@app.get('/status')
async def get_status():
    '''Returns api status : 1 --> api running correctly'''
    return 1

@app.get('/authorization')
async def get_user_authorization(authorized : bool = Depends(verify_token)):
    '''Return "authorized" if user is authentified and authorized, return exception if not'''
    if authorized:
        return {"detail" : "authorized"}

@app.post('/v1/rainTomorrow/predict')
async def get_v1_predict(item: V1Item, authorized : bool = Depends(verify_token)):
    '''If user is authorized, return the v1 prediction'''
    if authorized:
        item_dict = item.dict()
        my_model = RainsModelV1()
        transform_item = my_model.transformCatValues(item_dict)
        rainTomorrowV1 = my_model.predict(transform_item)

        if rainTomorrowV1 == 0:
            return {"detail" : "No"}
        else:
            return {"detail" : "Yes"}

@app.post('/v2/rainTomorrow/predict')
async def get_v2_predict(item: V2Item, authorized : bool = Depends(verify_token)):
    '''If user is authorized, return the v2 prediction'''
    if authorized:
        item_dict = item.dict()
        my_model = RainsModelV2()
        transform_item = my_model.transformCatValues(item_dict)
        rainTomorrowV2 = my_model.predict(transform_item)

        if rainTomorrowV2 == 0:
            return {"detail" : "No"}
        else:
            return {"detail" : "Yes"}

