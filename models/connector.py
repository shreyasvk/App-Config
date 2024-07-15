from pydantic import BaseModel, Field
from typing import List, Optional

class Connector(BaseModel):
    connector_type: str
    short_name: str
    description: str
    min_power_rating: float
    max_power_rating: float
    voltage_range: str
    current_range: str
    standard: str

class ConnectorResponse(BaseModel):
    ev_connector_types: List[Connector]
    
