from api.data.database import read_query, insert_query, update_query
from api.data.models import Calendar,Event, TeacherShow, CalendarById, EventChange, CalendarChange, EventCreate


def get_all_calendars_students(student_id):
    courses=read_query("select group_concat(distinct courses_id) from users_has_courses where users_id=? and subscriptions_id=1",(student_id,))
    if courses==[(None,)]:
       return []
    list_of_courses=[int(x) for x in courses[0][0].split(",")]
    calendars=[]
    for x in list_of_courses:
        calendar_data=read_query("select id,name,course_id,owner from calendars where course_id=?",(x,))
        if calendar_data!=[]:
         calendar=(Calendar.read_from_query_result(*row) for row in calendar_data)
         calendars.append(calendar)
    return calendars

def get_all_callendars_teacher(teacher_id):
    courses=read_query("select group_concat(distinct id) from courses where owner=?",(teacher_id,))
    if courses==[(None,)]:
       return []
    list_of_courses=[int(x) for x in courses[0][0].split(",")]
    calendars=[]
    for x in list_of_courses:
        calendar_data=read_query("select id,name,course_id,owner from calendars where course_id=?",(x,))
        if calendar_data!=[]:
         calendar=(Calendar.read_from_query_result(*row) for row in calendar_data)
         calendars.append(calendar)
    return calendars 

def get_all_calendars_admin():
    calendars=[]
    calendar_data=read_query("select id,name,course_id,owner from calendars")
    if calendar_data!=[]:
     for x in calendar_data:
      calendar=(Calendar.read_from_query_result(*x))
      calendars.append(calendar)
    return calendars   

def create_calendar(calendar:Calendar,user_id):
    insert_query("insert into calendars(name,owner,course_id) values(?,?,?)",(calendar.name,user_id,calendar.course_id))

def get_calendar_by_id(calendar_id):
    calendar_and_teacher_data=read_query("select c.id,c.name,c.course_id,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from calendars c join users u on c.owner=u.id where c.id=?",(calendar_id,))
    if calendar_and_teacher_data==[]:
        return None
    owner=(TeacherShow.read_from_query_result(*calendar_and_teacher_data[0][3:]))
    event_data=read_query("select id,name,start,end,link from events where calendar_id=?",(calendar_and_teacher_data[0][0],))
    events=[]
    for x in event_data:
        event=(Event.read_from_query_result(*x))
        events.append(event)
    calendar=CalendarById.read_from_query_result(*calendar_and_teacher_data[0][:3],owner=owner,events=events)
    return calendar

def create_event_in_calendar(event:EventCreate,calendar_id):
    id=insert_query("insert into events(name,calendar_id,start,end,link) values(?,?,?,?,?)",(event.name,calendar_id,event.start,event.end,event.link_to_event))
    return (Event.read_from_query_result(id=id,name=event.name,start=event.start,end=event.end,link_to_event=event.link_to_event))


def modify_event(event_id,event:EventChange):
    if event.name:
        update_query("update events set name=? where id=?",(event.name,event_id))
    if event.start:
        update_query("update events set start=? where id=?",(event.start,event_id))
    if event.end:
       update_query("update events set end=? where id=?",(event.end,event_id))
    if event.link_to_event:
        update_query("update events set link=? where id=?",(event.link_to_event,event_id))


def delete_event(event_id):
    update_query("delete from events where id=?",(event_id,))


def modify_calendar(calendar_id,calendar:CalendarChange):
    update_query("update calendars set owner=? where id=?",(calendar.owner_id,calendar_id))

def get_event_by_id(event_id):
    event_data=read_query("select id,name,start,end,link from events where id=?",(event_id,))
    if event_data==[]:
        return None
    return (Event.read_from_query_result(*row) for row in event_data)


    


