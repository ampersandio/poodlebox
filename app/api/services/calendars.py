from api.data.models import (
    Calendar,
    Event,
    EventChange,
    CalendarChange,
    EventCreate,
    CalendarCreate
)
from api.data import database

def get_all_calendars_students(student_id,db=None):
    """Get all the calendars for the coureses the student is currently enrolled in"""
    if db is None:
        db=database.read_query
    data = db(
        "select id,name,course_id,owner from calendars where course_id in (select distinct course_id from users_has_courses where users_id=? and subscriptions_id=1)",(student_id,)
    )
    if data==[]:
        return []
    calendars = []
    for x in data:
         calendar=Calendar.read_from_query_result(*x)
         calendars.append(calendar)
    return calendars


def get_all_callendars_teacher(teacher_id,db=None):
    """Get all the calendars that the teacher is an owner of"""
    if db is None:
        db=database.read_query
    data = db(
        "select id,name,course_id,owner from calendars where owner=?", (teacher_id,)
    )
    if data == []:
        return []
    calendars = []
    for x in data:
            calendar=Calendar.read_from_query_result(*x)
            calendars.append(calendar)
    return calendars 


def get_all_calendars_admin(db=None):
    '''Get all the calendars in the database'''
    if db is None:
        db=database.read_query
    calendars=[]
    calendar_data=db("select id,name,course_id,owner from calendars")
    if calendar_data!=[]:
        for x in calendar_data:
            calendar=Calendar.read_from_query_result(*x)
            calendars.append(calendar)
    return calendars   


def create_calendar(calendar: CalendarCreate, user_id,db=None):
    """Create a calendar"""
    if db is None:
        db=database.insert_query
    db(
        "insert into calendars(name,owner,course_id) values(?,?,?)",
        (calendar.name, user_id, calendar.course_id),
    )


def get_calendar_by_id(calendar_id,db=None):
    """Get a calendar by its id"""
    if db is None:
        db=database.read_query
    data= db(
        "select id,name,course_id,owner from calendars where id=?",
        (calendar_id,)
    )
    if data==[]:
        return None
    calendar=Calendar.read_from_query_result(*data[0])
    return calendar


def get_events_by_calendar_id(calendar_id,db=None):
    ''''Get events for a specific calendar'''
    if db is None:
        db=database.read_query
    data=db("select id,name,start,end,link from events where calendar_id=?",(calendar_id,))
    if data==[]:
        return []
    events=[]
    for x in data:
        event=Event.read_from_query_result(*x)
        events.append(event)
    return events


def create_event_in_calendar(event: EventCreate, calendar_id, db=None):
    """Create an event in a particular calendar"""
    if db is None:
        db=database.insert_query
    id = db(
        "insert into events(name,calendar_id,start,end,link) values(?,?,?,?,?)",
        (event.name, calendar_id, event.start, event.end, event.link_to_event),
    )
    return Event.read_from_query_result(
        id=id,
        name=event.name,
        start=event.start,
        end=event.end,
        link_to_event=event.link_to_event,
    )


def modify_event(event_id, event: EventChange,db=None):
    """Change the details of a specific event"""
    if db is None:
        db=database.update_query
    if event.name:
        db("update events set name=? where id=?", (event.name, event_id))
    if event.start:
        db("update events set start=? where id=?", (event.start, event_id))
    if event.end:
        db("update events set end=? where id=?", (event.end, event_id))
    if event.link_to_event:
        db(
            "update events set link=? where id=?", (event.link_to_event, event_id)
        )


def delete_event(event_id,db=None):
    """Delete an event from the database"""
    if db is None:
        db=database.update_query
    db("delete from events where id=?", (event_id,))


def modify_calendar(calendar_id, calendar: CalendarChange,db=None):
    """Change the owner of a calendar"""
    if db is None:
        db=database.update_query
    db(
        "update calendars set owner=? where id=?", (calendar.owner_id, calendar_id)
    )


def get_event_by_id(event_id,db=None):
    """Get an event by its id"""
    if db is None:
        db=database.read_query
    event_data = db(
        "select id,name,start,end,link from events where id=?", (event_id,)
    )
    if event_data == []:
        return None
    return next((Event.read_from_query_result(*row) for row in event_data),None)
