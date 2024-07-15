from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class EVErrorCodeResponse(BaseModel):
    id: str = Field(..., alias="_id")
    error_code: str
    charger_type: str
    description: str
    troubleshooting_steps: str
    charger_power_type: Literal["AC", "DC"]
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: str}
    }

class EVErrorCodeCreate(BaseModel):
    error_code: str
    charger_type: str
    description: str
    troubleshooting_steps: str
    charger_power_type: Literal["AC", "DC"]
    status: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "error_code": "E001",
                "charger_type": "CCS",
                "description": "Communication error between charger and vehicle",
                "troubleshooting_steps": "1. Check cable connection\n2. Restart charging process\n3. Contact support if issue persists",
                "charger_power_type": "DC",
                "status": True
            }
        }
    }

class EVErrorCodeUpdate(BaseModel):
    error_code: Optional[str] = None
    charger_type: Optional[str] = None
    description: Optional[str] = None
    troubleshooting_steps: Optional[str] = None
    charger_power_type: Optional[Literal["AC", "DC"]] = None
    status: Optional[bool] = None