import api.utils.constants as constants

from fastapi import APIRouter, Depends, Response, HTTPException
from api.data.models import (
    User,
    EventChange,
    CalendarChange,
    CalendarCreate,
    EventCreate,
)
from fastapi.responses import JSONResponse
from api.services.authorization import get_current_user
from api.services.calendars import (
    get_all_calendars_admin,
    get_all_calendars_students,
    get_all_callendars_teacher,
    create_calendar,
    create_event_in_calendar,
    modify_event,
    delete_event,
    get_calendar_by_id,
    get_event_by_id,
    get_events_by_calendar_id
)
from api.services.courses import get_course_by_id
from api.services.students import get_students_active_courses

calendar_router = APIRouter(prefix="/calendars", tags=["Calendars"])


@calendar_router.get("/")
def get_all_calendars(current_user: User = Depends(get_current_user)):
    if current_user.role == constants.ADMIN_ROLE:
        return get_all_calendars_admin()
    elif current_user.role == constants.TEACHER_ROLE:
        return get_all_callendars_teacher(current_user.id)
    return get_all_calendars_students(current_user.id)


@calendar_router.post("/")
def create_calendars(
    calendar: CalendarCreate, current_user: User = Depends(get_current_user)
):
    if current_user.role == constants.STUDENT_ROLE:
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if get_course_by_id(calendar.course_id) is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)
    if (
        get_course_by_id(calendar.course_id).teacher.id != current_user.id
        and current_user.role == constants.TEACHER_ROLE
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    create_calendar(calendar, current_user.id)
    return JSONResponse(
        status_code=201, content={"msg": "Calendar created successfully"}
    )


@calendar_router.get("/{calendar_id}")
def get_calendar_by_calendar_id(
    calendar_id: int, current_user: User = Depends(get_current_user)
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail={"msg": constants.SECTION_ACCESS_DENIED_DETAIL}
        )
    return result

@calendar_router.get("/{calendar_id}/events")
def get_events_for_calendar(calendar_id:int,current_user: User = Depends(get_current_user)):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail={"msg": constants.SECTION_ACCESS_DENIED_DETAIL}
        )
    
    return get_events_by_calendar_id(calendar_id)



@calendar_router.put("/{calendar_id}")
def change_calendar_owner(
    calendar_id: int,
    calendar: CalendarChange,
    current_user: User = Depends(get_current_user),
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    change_calendar_owner(calendar_id, calendar)
    return JSONResponse(status_code=200, content={"msg": "Owner changed successfully"})


@calendar_router.post("/{calendar_id}/events")
def add_event(
    calendar_id: int, event: EventCreate, current_user: User = Depends(get_current_user)
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    return create_event_in_calendar(event, calendar_id)


@calendar_router.get("/{calendar_id}/events/{event_id}")
def get_event_by_event_id(
    calendar_id: int, event_id: int, current_user: User = Depends(get_current_user)
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=constants.EVENT_NOT_FOUND_DETAIL)
    return event


@calendar_router.put("{calendar_id}/events/{event_id}")
def change_event(
    calendar_id: int,
    event_id: int,
    event: EventChange,
    current_user: User = Depends(get_current_user),
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=constants.EVENT_NOT_FOUND_DETAIL)
    modify_event(event_id, event)
    return JSONResponse(status_code=200, content={"msg": "Event changed successfully"})


@calendar_router.delete("{calendar_id}/events/{event_id}")
def delete_an_event(
    calendar_id: int, event_id: int, current_user: User = Depends(get_current_user)
):
    result = get_calendar_by_id(calendar_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.CALENDAR_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.course_id not in get_students_active_courses(current_user.id)
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    if (
        current_user.role == constants.TEACHER_ROLE
        and result.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL
        )
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=constants.EVENT_NOT_FOUND_DETAIL)
    delete_event(event_id)
    return Response(status_code=204)
