from typing import Literal
from fastapi import FastAPI, Header, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from routers import vehicle_brand
from schemas.vehicle_brand import VehicleBrandCreate, VehicleBrandUpdate

app = FastAPI()

resource_routers = {
    "vehicle_brand": vehicle_brand.router,
    # "vehicle_model": vehicle_model.router,
    # "amenities": amenities.router,
    # "cities": cities.router,
}

async def get_body(request: Request):
    return await request.json()

@app.api_route("/v1/resources", methods=["GET", "POST"])
@app.api_route("/v1/resources/{item_id}", methods=["GET", "PUT", "DELETE", "PATCH"])
async def dynamic_crud(
    request: Request,
    item_id: str = None,
    x_resource_type: Literal["vehicle_brand", "vehicle_model", "amenities", "cities", "connector", "charger", "states"] = Header(...),
    body: dict = Depends(get_body)
):
    router = resource_routers[x_resource_type]
    
    for route in router.routes:
        if request.method in route.methods:
            if item_id and "{brand_id}" in route.path:
                if request.method == "PUT":
                    return await route.endpoint(item_id, body)
                elif request.method == "PATCH":
                    return await route.endpoint(item_id, body)
                elif request.method == 'GET':
                    return await route.endpoint(item_id)                
                else:
                    return await route.endpoint(item_id)
            elif not item_id and "{brand_id}" not in route.path:
                if request.method == "GET":
                    return await route.endpoint()
                elif request.method == "POST":
                    return await route.endpoint(body)