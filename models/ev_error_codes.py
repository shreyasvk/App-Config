from pydantic import BaseModel, Field
from datetime import datetime
from config import PyObjectId
from typing import Annotated, Literal

class EVErrorCode(BaseModel):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    error_code: str
    charger_type: str
    description: str
    troubleshooting_steps: str
    charger_power_type: Literal["AC", "DC"]
    status: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }