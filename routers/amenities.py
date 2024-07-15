from fastapi import APIRouter, HTTPException
from config import amenities_collection
from models.amenities import Amenity
from schemas.amenities import AmenityResponse, AmenityCreate, AmenityUpdate
from datetime import datetime

class Amenities(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/v1/resources"
        
    async def get_all(self):
        amenities = await amenities_collection.find().to_list(1000)
        return [AmenityResponse(**amenity) for amenity in amenities]

    async def get_one(self, amenity_id: str):
        amenity = await amenities_collection.find_one({"_id": amenity_id})
        if amenity is None:
            raise HTTPException(status_code=404, detail="Amenity not found")
        return AmenityResponse(**amenity)
    
    async def create(self, amenity: dict):
        validated_data = AmenityCreate(**amenity)
        current_time = datetime.now()
        new_amenity = Amenity(
            **validated_data.model_dump(),
            created_at=current_time,
            updated_at=current_time
        )
        result = await amenities_collection.insert_one(new_amenity.model_dump(by_alias=True))
        created_amenity = await amenities_collection.find_one({"_id": result.inserted_id})
        return AmenityResponse(**created_amenity)

    async def delete(self, amenity_id: str):
        result = await amenities_collection.delete_one({"_id": amenity_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Amenity not found")
        return None 

    async def update(self, amenity_id: str, amenity: dict):
        validated_data = AmenityCreate(**amenity)
        update_data = validated_data.model_dump()
        update_data["updated_at"] = datetime.now()
        result = await amenities_collection.update_one(
            {"_id": amenity_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Amenity not found")
        updated_amenity = await amenities_collection.find_one({"_id": amenity_id})
        return AmenityResponse(**updated_amenity)

    async def partial_update(self, amenity_id: str, amenity: dict):
        validated_data = AmenityUpdate(**amenity)
        update_data = validated_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")
        result = await amenities_collection.update_one(
            {"_id": amenity_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Amenity not found")
        updated_amenity = await amenities_collection.find_one({"_id": amenity_id})
        return AmenityResponse(**updated_amenity)

router = Amenities()