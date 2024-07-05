from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class VehicleBrandResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    logo_url: str
    website_url: str
    country_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: str}
    }

class VehicleBrandCreate(BaseModel):
    name: str
    logo_url: str
    website_url: str
    country_code: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Tesla",
                "logo_url": "https://example.com/tesla_logo.png",
                "website_url": "https://www.tesla.com",
                "country_code": "US",
            }
        }
    }
