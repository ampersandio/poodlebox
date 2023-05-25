from fastapi import APIRouter, Depends, HTTPException
from api.data.models import User
from api.services.authorization import get_current_user
from api.services.users import view_add

ads_router = APIRouter(prefix="/ads", tags=["Ads"])

@ads_router.get("/")
def get_users_add(current_user: User = Depends(get_current_user)):
    return view_add(current_user.id)