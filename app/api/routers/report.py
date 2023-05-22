from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from api.services.authorization import get_current_user
from api.data.models import User, TeachersReport
from api.services.report import get_teachers_report


report_router = APIRouter(prefix='/report')


@report_router.get('/', tags=['Teachers'])
def get_report(current_user: Annotated[User, Depends(get_current_user)]) -> TeachersReport:
    if current_user.role.lower() != 'teacher':
        raise HTTPException(status_code=400, detail='Reports are currently only available for teachers')
    
    teachers_report = get_teachers_report(current_user)
    if teachers_report is None:
        raise HTTPException(status_code=204, detail='You either currently own no courses, or there are no students enrolled in any of your courses')

    return teachers_report
