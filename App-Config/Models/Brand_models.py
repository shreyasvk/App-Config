from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

class UpdateVehicleBrand(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    country_code: Optional[str] = None
    updated_at: Optional[datetime] = None

class VehicleBrand(BaseModel):
    id: str
    name: str
    logo_url: str
    website_url: str
    country_code: str
    created_at: datetime = datetime.now()
    updated_at: datetime
