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
@app.api_route("/v1/resources/{item_id}", methods=["GET", "PUT", "DELETE"])
async def dynamic_crud(
    request: Request,
    item_id: str = None,
    x_resource_type: Literal["vehicle_brand", "vehicle_model", "amenities", "cities"] = Header(...),
    body: dict = Depends(get_body)
):
    if x_resource_type not in resource_routers:
        raise HTTPException(status_code=400, detail=f"Invalid resource type: {x_resource_type}")
    
    router = resource_routers[x_resource_type]
    
    for route in router.routes:
        if request.method in route.methods:
            if item_id and "{brand_id}" in route.path:
                if request.method == "PUT":
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
    
    raise HTTPException(status_code=405, detail="Method not allowed for this resource type")