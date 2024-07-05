from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from Routers import vehicle_brand

app = FastAPI()

router = APIRouter()
app.include_router(router, prefix="/resource")
resource_types = [
    "Vehicle_Brand",
    "Vehicle_Model",
    "States",
    "Connector",
    "Cities",
    "Charger",
    "Amenities"
]

@app.get("/resources")
def get_all_brands(x_resource_type: str = Header(None)):
    if x_resource_type == "Vehicle_Brand":
        return vehicle_brand.get_all_brands()

@app.post("/resources")
def create_brand(x_resource_type: str = Header(None)):
    if x_resource_type == "Vehicle_Brand": 
        return vehicle_brand.create_brand()
    