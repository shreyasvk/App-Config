from pydantic import BaseModel, Field
from datetime import datetime
from config import PyObjectId
from typing import Annotated

class Amenity(BaseModel):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    description: str
    status: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }