from fastapi import APIRouter, HTTPException
from databases.vehicle_brand import PyObjectId, vehicle_brand_collection
from models.vehicle_brand import VehicleBrand
from schemas.vehicle_brand import VehicleBrandResponse, VehicleBrandCreate
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/v1/resources", response_model=List[VehicleBrandResponse])
async def get_vehicle_brands():
    vehicle_brands = await vehicle_brand_collection.find().to_list(1000)
    return vehicle_brands
    pass

@router.post("/v1/resources", response_model=VehicleBrandResponse, status_code=201)
async def create_vehicle_brand(vehicle_brand: VehicleBrandCreate):
    current_time = datetime.utcnow()
    
    new_brand = VehicleBrand(
        **vehicle_brand.model_dump(),
        created_at=current_time,
        updated_at=current_time
    )

    result = await vehicle_brand_collection.insert_one(new_brand.model_dump(by_alias=True))
    
    if result.inserted_id:
        created_brand = await vehicle_brand_collection.find_one({"_id": result.inserted_id})
        return created_brand
    else:
        raise HTTPException(status_code=400, detail="Failed to create vehicle brand")
    pass