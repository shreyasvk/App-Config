from bson import ObjectId
from fastapi import APIRouter, HTTPException
from databases.vehicle_brand import vehicle_brand_collection
from models.vehicle_brand import VehicleBrand
from schemas.vehicle_brand import VehicleBrandResponse, VehicleBrandCreate, VehicleBrandUpdate
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/v1/resources", response_model=List[VehicleBrandResponse])
async def get_vehicle_brands():
    vehicle_brands = await vehicle_brand_collection.find().to_list(1000)
    return [VehicleBrandResponse(**brand) for brand in vehicle_brands]

@router.get("/v1/resources/{brand_id}", response_model=VehicleBrandResponse)
async def get_vehicle_brand(brand_id: str):
    brand = await vehicle_brand_collection.find_one({"_id": brand_id})
    if brand is None:
        raise HTTPException(status_code=404, detail="Vehicle brand not found")
    return VehicleBrandResponse(**brand)

@router.post("/v1/resources", response_model=VehicleBrandResponse, status_code=201)
async def create_vehicle_brand(vehicle_brand: dict):
    validated_data = VehicleBrandCreate(**vehicle_brand)
    current_time = datetime.now()
        
    new_brand = VehicleBrand(
        **validated_data.model_dump(),
        created_at=current_time,
        updated_at=current_time
    )
    result = await vehicle_brand_collection.insert_one(new_brand.model_dump(by_alias=True))
    created_brand = await vehicle_brand_collection.find_one({"_id": result.inserted_id})
    return VehicleBrandResponse(**created_brand)

@router.delete("/v1/resources/{brand_id}", status_code=204)
async def delete_vehicle_brand(brand_id: str):
    result = await vehicle_brand_collection.delete_one({"_id": brand_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vehicle brand not found")
    return None 

@router.put("/v1/resources/{brand_id}", response_model=VehicleBrandResponse)
async def update_vehicle_brand(brand_id: str, vehicle_brand: dict):

    validated_data = VehicleBrandCreate(**vehicle_brand)
    update_data = validated_data.model_dump()
    update_data["updated_at"] = datetime.now()

    result = await vehicle_brand_collection.update_one(
        {"_id": brand_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vehicle brand not found")

    updated_brand = await vehicle_brand_collection.find_one({"_id": brand_id})
    return VehicleBrandResponse(**updated_brand)

@router.patch("/v1/resources/{brand_id}", response_model=VehicleBrandResponse)
async def partial_update_vehicle_brand(brand_id: str, vehicle_brand: dict):

    validated_data = VehicleBrandUpdate(**vehicle_brand)
    update_data = validated_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now()

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")

    result = await vehicle_brand_collection.update_one(
        {"_id": brand_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vehicle brand not found")
    updated_brand = await vehicle_brand_collection.find_one({"_id": brand_id})
    return VehicleBrandResponse(**updated_brand)


