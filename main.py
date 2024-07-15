from typing import Literal
from fastapi import FastAPI, HTTPException, Header, Request, Depends
from routers import vehicle_brand,vehicle_model,amenities,ev_error_codes, connector

app = FastAPI()

resource_routers = {
    "vehicle_brand": vehicle_brand.router,
    "vehicle_model": vehicle_model.router,
    "amenities": amenities.router,
    "connector": connector.router,
    "ev_error_code": ev_error_codes.router
}

async def get_body(request: Request):
    return await request.json()

@app.api_route("/v1/resources", methods=["GET", "POST"])
@app.api_route("/v1/resources/{item_id}", methods=["GET", "PUT", "DELETE", "PATCH"])
async def dynamic_crud(
    request: Request,
    item_id: str = None,
    x_resource_type: Literal["vehicle_brand", "vehicle_model", "amenities",  "connector", "ev_error_code"] = Header(...),
    body: dict = Depends(get_body)
):
    try:
        router = resource_routers[x_resource_type]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid Resource Type")
    
    method = request.method
    try:
        if item_id:
            if method == "GET":
                return await router.get_one(item_id)
            elif method == "PUT":
                return await router.update(item_id, body)
            elif method == "PATCH":
                return await router.partial_update(item_id, body)
            elif method == "DELETE":
                return await router.delete(item_id)
        else:
            if method == "GET":
                return await router.get_all()
            elif method == "POST":
                return await router.create(body)
        
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    except AttributeError:
        raise HTTPException(status_code=501, detail=f"Method {method} not implemented for this resource")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing {method} request: {str(e)}")