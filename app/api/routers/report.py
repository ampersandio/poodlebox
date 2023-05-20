from typing import Annotated

from fastapi import APIRouter, Depends
from services.authorization import get_current_user
from data.models import User, TeachersReport


report_router = APIRouter(prefix='/report')


@report_router.get('/')
def get_report(current_user: Annotated[User, Depends(get_current_user)]) -> TeachersReport:
    pass