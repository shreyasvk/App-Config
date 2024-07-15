from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class VehicleModelResponse(BaseModel):
    id: str = Field(..., alias="_id")
    brand_id: str
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
    features: Dict[str, Any]
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: str},
        "arbitrary_types_allowed": True
    }

class VehicleModelCreate(BaseModel):
    brand_id: str
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
    features: Dict[str, Any]
    status: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_id": "5f8a3d5e6c7d8e9f0a1b2c3d",
                "model": "Model S",
                "launch_year": 2012,
                "battery_capacity": 100.0,
                "charger_type": ["AC", "DC"],
                "connector_type": ["Type 2", "CCS"],
                "charging_time": "1 hour",
                "range": "400 km",
                "mileage": 0.2,
                "motor_type": "FourWheeler",
                "v2g_support": True,
                "v2x_support": True,
                "v2i_support": True,
                "features": {
                    "autopilot": True,
                    "heated_seats": True
                },
                "status": True
            }
        },
        "arbitrary_types_allowed": True
    }

class VehicleModelUpdate(BaseModel):
    brand_id: Optional[str] = None
    model: Optional[str] = None
    launch_year: Optional[int] = None
    battery_capacity: Optional[float] = None
    charger_type: Optional[List[str]] = None
    connector_type: Optional[List[str]] = None
    charging_time: Optional[str] = None
    range: Optional[str] = None
    mileage: Optional[float] = None
    motor_type: Optional[str] = None
    v2g_support: Optional[bool] = None
    v2x_support: Optional[bool] = None
    v2i_support: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None
    status: Optional[bool] = None

    model_config = {
        "arbitrary_types_allowed": True
    }
    
    
    