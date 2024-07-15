from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Annotated
from config import PyObjectId

class VehicleModel(BaseModel):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    brand_id: PyObjectId
    model: str
    launch_year: int
    battery_capacity: float
    charger_type: List[str]
    connector_type: List[str]
    charging_time: str
    range: str
    mileage: float
    motor_type: str
    v2g_support: bool
    v2x_support: bool
    v2i_support: bool
    features: Dict[str, any]
    status: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }