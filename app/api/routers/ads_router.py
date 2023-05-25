from fastapi import APIRouter, Depends, HTTPException
from api.data.models import User
from api.services.authorization import get_current_user
from api.services.users import view_add

ads_router = APIRouter(prefix="/ads", tags=["Ads"])

@ads_router.get("/")
def get_students_add(current_user: User = Depends(get_current_user)):
    if current_user.role!="student":
        raise HTTPException(status_code=403,detail="You don't have access to this section")
    return view_add(current_user.id)