from fastapi import APIRouter, Depends, HTTPException
from api.data.models import User
from api.services.authorization import get_current_user
from api.services.users import view_ad

ads_router = APIRouter(prefix="/ads", tags=["Ads"])

@ads_router.get("/")
def get_users_ad(current_user: User = Depends(get_current_user)):
    result=view_ad(current_user.id)
    if result is None:
        raise HTTPException(status_code=404,detail="No ad to show")
    return view_ad(current_user.id)