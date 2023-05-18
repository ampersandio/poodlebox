from fastapi import APIRouter
from api.routers.authorization import authorization_router

api_router = APIRouter(prefix="/api")

api_router.include_router(authorization_router)

@api_router.get("/")
def sub_router():
    return {"this is api_router.py"}