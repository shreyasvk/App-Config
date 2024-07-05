from typing import Literal
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from routers import vehicle_brand
from schemas.vehicle_brand import VehicleBrandCreate

app= FastAPI()

resource_routers = {
    "vehicle_brand": vehicle_brand.router,
#     "vehicle_model": vehicle_model.router,
#     "amenities": amenities.router,
#     "cities": cities.router,
}

dynamic_router = APIRouter()
async def get_body(request: Request):
    return await request.json()

@dynamic_router.api_route("/v1/resources", methods=["GET", "POST"])
@dynamic_router.api_route("/v1/resources/{item_id}", methods=["GET", "PUT", "DELETE"])
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
            if item_id and "{item_id}" in route.path:
                if request.method == "PUT":
                    return await route.endpoint(item_id, VehicleBrandCreate(**body))
                else:
                    return await route.endpoint(item_id)
            elif not item_id and "{item_id}" not in route.path:
                if request.method == "GET":
                    return await route.endpoint()
                elif request.method == "POST":
                    return await route.endpoint(VehicleBrandCreate(**body))
    
    raise HTTPException(status_code=405, detail="Method not allowed for this resource type")
app.include_router(dynamic_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)