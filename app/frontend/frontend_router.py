from fastapi import APIRouter

frontend_router = APIRouter(include_in_schema=False,prefix="/poodlebox")

@frontend_router.get("/")
def sub_router():
    return {"this is frontend_router.py"}