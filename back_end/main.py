from fastapi import FastAPI

app = FastAPI()

from routers import courses_router
app.include_router(courses_router.courses_router)