import requests
from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path

url = "https://playgroundvwtestapp.azurewebsites.net/vehicle/"
url_find_by_status = url + "findByStatus"

class Status(str, Enum):
    available = "Available"
    sold = "Sold"



app = FastAPI()



@app.get("/vehicle/{vin}")
async def getVehicle(vin: Annotated[str, Path(title="vin")]):
   res = requests.request("GET", url + vin)
   return res.json()