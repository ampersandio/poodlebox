from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

@api_router.get("/")
def sub_router():
    return {"this is api_router.py"}