# Virtualization - Virtualize the API on your machine
from enum import Enum
from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BaseModel
import requests
import json
import uvicorn

url = "https://playgroundvwtestapp.azurewebsites.net/vehicle/"
url_find_by_status = url + "findByStatus"


class Status(str, Enum):
    available = "Available"
    sold = "Sold"


class Vehicle(BaseModel):
    vin: str
    name: str
    status: Status

app = FastAPI()

@app.head("/")
@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.get("/vehicle/findByStatus")
async def findByStatusVehicle(stati: Status):
    if stati is Status.available:
        res = requests.request("GET", url_find_by_status + "?stati=Available")
    elif stati is Status.sold:
        res = requests.request("GET", url_find_by_status + "?stati=Sold")
    return res.json()


@app.get("/vehicle/{vin}")
async def getVehicle(vin: Annotated[str, Path(title="vin")]):
    res = requests.request("GET", url + vin)
    return res.json()


# VIRTUALIZATION - Ex 1. Modify the API that you now run locally in such way that while creating a VIN
# you receive the error code 500.
@app.post("/vehicle", status_code=500)
async def createVehicle(veh: Vehicle):
    #vin_dict = {"vin": veh.vin, "name": veh.name, "status": veh.status}
    #res = requests.post(url, json=vin_dict)
    res = {"vin": veh.vin, "name": veh.name, "status": "-", "id": "-"}
    return res


@app.put("/vehicle")
async def updateVehicle(veh: Vehicle):
    vin_dict = {"vin": veh.vin, "name": veh.name, "status": veh.status}
    res = requests.put(url, json=vin_dict)
    return res.json()

@app.delete("/vehicle/deleteAll")
async def deleteAllVehicles():
    response_available = requests.request("GET", url_find_by_status + "?stati=Available")
    response_sold = requests.request("GET", url_find_by_status + "?stati=Sold")
    response_available = json.loads(response_available.text)
    response_sold = json.loads(response_sold.text)
    for available in response_available:
        res = requests.request("DELETE", url + available["vin"])
        print(f"Available {available['vin']} deleted")
    for sold in response_sold:
        res = requests.request("DELETE", url + sold["vin"])
        print(f"Sold {sold['vin']} deleted")
    return {"status": "Deleted All"}

@app.delete("/vehicle/{vin}")
async def deleteVehicle(vin: Annotated[str, Path(title="vin")]):
    res = requests.request("DELETE", url + vin)
    res.json()

if __name__ == "main":
    uvicorn.run(app, host="127:0.0.1", port=8000)