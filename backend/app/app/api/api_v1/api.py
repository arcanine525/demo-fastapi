from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, car_brand


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(car_brand.router, prefix="/car_brands", tags=["car_brands"])
