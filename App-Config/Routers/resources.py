from fastapi import APIRouter,HTTPException, Header
from Routers import vehicle_brand

router=APIRouter()


@router.get("/resou")
def get_all_brands(x_resource_type: str = Header(None)):
    if x_resource_type==vehicle_brand:
        return vehicle_brand.get_all_brands()

@router.get("/")
def create_brand(x_resource_type: str = Header(None)):
    if x_resource_type==vehicle_brand:
        return vehicle_brand.create_brand()
    
# @router.get("/")
# def resource_type(chosen_subresource: str):
#     if chosen_subresource==vehicle_brand:
#         return vehicle_brand.get_all_brands()
# @router.post("/")
# def resource_type(chosen_subresource: str):
#     if chosen_subresource==vehicle_brand:
#         return vehicle_brand.create_brand()
    