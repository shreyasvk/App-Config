from bson import ObjectId
from fastapi import HTTPException,APIRouter
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from Models.Brand_models import  VehicleBrand, UpdateVehicleBrand

router=APIRouter()

MONGO_DETAILS = "mongodb+srv://Shreyas:Shreyas123@fasterapi.i2bp8f5.mongodb.net/"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.my_database
vehicle_brand_collection = database.get_collection("Vehicle_Brand")

def vehicle_brand(brand) -> dict:
    return {
        "id": str(brand["_id"]),
        "name": brand["name"],
        "logo_url": brand["logo_url"],
        "website_url": brand["website_url"],
        "country_code": brand["country_code"],
        "created_at": brand["created_at"],
        "updated_at": brand.get("updated_at")
    }

@router.post("/")
async def create_brand(brand: VehicleBrand):
    brand_dict = brand.dict()
    brand_dict["created_at"] = datetime.now()
    result = await vehicle_brand_collection.insert_one(brand_dict)
    new_brand = await vehicle_brand_collection.find_one({"_id": result.inserted_id})
    return vehicle_brand(new_brand)

@router.get("/")
async def get_all_brands():
    brands = []
    async for brand in vehicle_brand_collection.find():
        brands.append(VehicleBrand(brand))
    return brands

@router.get("/{id}")
async def get_brand(brand_id: str):
    brand = await vehicle_brand_collection.find_one({"_id": ObjectId(brand_id)})
    if brand:
        return brand
    raise HTTPException(status_code=404, detail="Brand not found")

@router.put("/{id}")
async def update_brand(brand_id: str, brand: VehicleBrand):
    brand_dict = brand.dict()
    brand_dict["updated_at"] = datetime.now()
    updated_brand = await vehicle_brand_collection.update_one(
        {"_id": ObjectId(brand_id)}, {"$set": brand_dict}
    )
    if updated_brand.modified_count == 1:
        new_brand = await vehicle_brand_collection.find_one({"_id": ObjectId(brand_id)})
        return new_brand
    raise HTTPException(status_code=404, detail="Brand not found")

@router.delete("/{id}")
async def delete_brand(brand_id: str):
    delete_result = await vehicle_brand_collection.delete_one({"_id": ObjectId(brand_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Brand deleted successfully"}
    raise HTTPException(status_code=404, detail="Brand not found")

@router.patch("/{id}")
async def partial_update_brand(brand_id: str, brand: UpdateVehicleBrand):
    brand_dict = {k: v for k, v in brand.dict().items() if v is not None}
    brand_dict["updated_at"] = datetime.now()
    updated_brand = await vehicle_brand_collection.update_one(
        {"_id": ObjectId(brand_id)}, {"$set": brand_dict}
    )
    if updated_brand.modified_count == 1:
        new_brand = await vehicle_brand_collection.find_one({"_id": ObjectId(brand_id)})
        return vehicle_brand(new_brand)
    raise HTTPException(status_code=404, detail="Brand not found")