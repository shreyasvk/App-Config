from fastapi import HTTPException, APIRouter
import yaml
from pathlib import Path
from models.connector import ConnectorResponse

def load_yaml() -> ConnectorResponse:
    yaml_path = Path(__file__).parent.parent / "connector.yaml"
    with yaml_path.open("r") as file:
        content = yaml.safe_load(file)
        return ConnectorResponse(**content)
    
class Connector(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/v1/resources"

    async def get_all(self):
        data = load_yaml()
        return data.ev_connector_types
    
    async def get_one(self, short_name: str):
        data = load_yaml()
        for connector in data.ev_connector_types:
            if connector.short_name == short_name:
                return connector
        raise HTTPException(status_code=404, detail="Connector not found")
router = Connector()