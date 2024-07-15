from fastapi import APIRouter, HTTPException
from config import vehicle_model_collection
from models.vehicle_model import VehicleModel
from config import vehicle_brand_collection
from schemas.vehicle_model import VehicleModelResponse, VehicleModelCreate, VehicleModelUpdate
from datetime import datetime

async def validate_id(brand_id: str):
    brand = await vehicle_brand_collection.find_one({"_id": brand_id})
    if not brand:
        raise HTTPException(status_code=400, detail=f"Brand with id {brand_id} does not exist")
    return str(brand["_id"])

class VehicleModels(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/v1/resources"

    async def get_all(self):
        vehicle_models = await vehicle_model_collection.find().to_list(1000)
        return [VehicleModelResponse(**model) for model in vehicle_models]

    async def get_one(self, model_id: str):
        model = await vehicle_model_collection.find_one({"_id": model_id})
        if model is None:
            raise HTTPException(status_code=404, detail="Vehicle model not found")
        return VehicleModelResponse(**model)
    
    async def create(self, vehicle_model: dict):
        validated_brand_id = await validate_id(vehicle_model['brand_id'])
        vehicle_model['brand_id'] = validated_brand_id

        validated_data = VehicleModelCreate(**vehicle_model)
        current_time = datetime.now()
        new_model = VehicleModel(
            **validated_data.model_dump(),
            created_at=current_time,
            updated_at=current_time
        )
        result = await vehicle_model_collection.insert_one(new_model.model_dump(by_alias=True))
        created_model = await vehicle_model_collection.find_one({"_id": result.inserted_id})
        return VehicleModelResponse(**created_model)

    async def delete(self, model_id: str):
        result = await vehicle_model_collection.delete_one({"_id": model_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle model not found")
        return None 

    async def update(self, model_id: str, vehicle_model: dict):
        validated_data = VehicleModelCreate(**vehicle_model)
        update_data = validated_data.model_dump()
        update_data["updated_at"] = datetime.now()
        result = await vehicle_model_collection.update_one(
            {"_id": model_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle model not found")
        updated_model = await vehicle_model_collection.find_one({"_id": model_id})
        return VehicleModelResponse(**updated_model)

    async def partial_update(self, model_id: str, vehicle_model: dict):
        validated_data = VehicleModelUpdate(**vehicle_model)
        update_data = validated_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")
        result = await vehicle_model_collection.update_one(
            {"_id": model_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle model not found")
        updated_model = await vehicle_model_collection.find_one({"_id": model_id})
        return VehicleModelResponse(**updated_model)

router = VehicleModels()