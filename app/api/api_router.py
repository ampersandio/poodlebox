from fastapi import APIRouter
from api.routers.authorization import authorization_router
from api.routers.courses_router import courses_router
from api.routers.students_router import students_router
from api.routers.report import report_router
from api.routers.admins_router import admins_router

api_router = APIRouter(prefix="/api")

api_router.include_router(authorization_router)
api_router.include_router(courses_router)
api_router.include_router(students_router)
api_router.include_router(report_router)
api_router.include_router(admins_router)



@api_router.get("/")
def sub_router():
    return {"this is api_router.py"}