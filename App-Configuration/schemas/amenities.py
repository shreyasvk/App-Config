from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AmenityResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    description: str
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: str}
    }

class AmenityCreate(BaseModel):
    name: str
    description: str
    status: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Free Wi-Fi",
                "description": "High-speed wireless internet access",
                "status": True
            }
        }
    }

class AmenityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None