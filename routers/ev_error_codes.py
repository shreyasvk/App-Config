from fastapi import APIRouter, HTTPException
from config import ev_error_codes_collection
from models.ev_error_codes import EVErrorCode
from schemas.ev_error_codes import EVErrorCodeResponse, EVErrorCodeCreate, EVErrorCodeUpdate
from datetime import datetime

class EVErrorCodes(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/v1/resources"
        
    async def get_all(self):
        error_codes = await ev_error_codes_collection.find().to_list(1000)
        return [EVErrorCodeResponse(**error_code) for error_code in error_codes]

    async def get_one(self, error_code_id: str):
        error_code = await ev_error_codes_collection.find_one({"_id": error_code_id})
        if error_code is None:
            raise HTTPException(status_code=404, detail="EV Error Code not found")
        return EVErrorCodeResponse(**error_code)
    
    async def create(self, error_code: dict):
        validated_data = EVErrorCodeCreate(**error_code)
        current_time = datetime.now()
        new_error_code = EVErrorCode(
            **validated_data.model_dump(),
            created_at=current_time,
            updated_at=current_time
        )
        result = await ev_error_codes_collection.insert_one(new_error_code.model_dump(by_alias=True))
        created_error_code = await ev_error_codes_collection.find_one({"_id": result.inserted_id})
        return EVErrorCodeResponse(**created_error_code)

    async def delete(self, error_code_id: str):
        result = await ev_error_codes_collection.delete_one({"_id": error_code_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="EV Error Code not found")
        return None 

    async def update(self, error_code_id: str, error_code: dict):
        validated_data = EVErrorCodeCreate(**error_code)
        update_data = validated_data.model_dump()
        update_data["updated_at"] = datetime.now()
        result = await ev_error_codes_collection.update_one(
            {"_id": error_code_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="EV Error Code not found")
        updated_error_code = await ev_error_codes_collection.find_one({"_id": error_code_id})
        return EVErrorCodeResponse(**updated_error_code)

    async def partial_update(self, error_code_id: str, error_code: dict):
        validated_data = EVErrorCodeUpdate(**error_code)
        update_data = validated_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")
        result = await ev_error_codes_collection.update_one(
            {"_id": error_code_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="EV Error Code not found")
        updated_error_code = await ev_error_codes_collection.find_one({"_id": error_code_id})
        return EVErrorCodeResponse(**updated_error_code)

router = EVErrorCodes()