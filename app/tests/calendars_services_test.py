import unittest
from api.services import calendars
from api.data.models import Calendar, Event, CalendarChange, CalendarCreate, EventChange, EventCreate


class CalendarServiceShould(unittest.TestCase):
    def test_get_all_calendars_studentsWithData(self):
        db= lambda q,id:[(1,"Python",2,2)]
        result=calendars.get_all_calendars_students(70,db)
        self.assertEqual(1,len(result))
    
    def test_get_all_calendars_studentsNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=calendars.get_all_calendars_students(3,db)
        self.assertEqual(expected,result)
    
    def test_get_all_calendarsAdminWithData(self):
        db=lambda q:[(9,"Java",2,2)]
        result=calendars.get_all_calendars_admin(db)
        self.assertEqual(1,len(result))
    
    def test_get_all_calendarsAdminNoData(self):
        db=lambda q:[]
        expected=[]
        result=calendars.get_all_calendars_admin(db)
        self.assertEqual(expected,result)
           
    def test_get_all_calendarsTeacherWithData(self):
        db=lambda q,id:[(1,"Python",2,2)]
        result=calendars.get_all_callendars_teacher(70,db)
        self.assertEqual(1,len(result))
    
    def test_get_all_calendarsTeacherNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=calendars.get_all_callendars_teacher(1,db)
        self.assertEqual(expected,result)

    def test_createCalendar(self):
        db=lambda q,calendar:[(1,)]
        calendar=CalendarCreate(name="Python",course_id=1)
        expected=None
        result=calendars.create_calendar(calendar,1,db)
        self.assertEqual(expected,result)
    
    def test_get_calendar_byIdWithData(self):
        db=lambda q,id:[(1,"Python",1,1)]
        data=[(1,"Python",1,1)]
        expected=Calendar.read_from_query_result(*data[0])
        result=calendars.get_calendar_by_id(1,db)
        self.assertEqual(expected,result)
    
    def test_get_calendar_byIdNoData(self):
        db=lambda q,id:[]
        expected=None
        result=calendars.get_calendar_by_id(1,db)
        self.assertEqual(expected,result)
    
    def test_get_events_by_calendarIdWithData(self):
        db=lambda q,id:[((1,"OOP","2023-06-15T10:00:00.898000","2023-06-15T14:00:00.898000","link"))]
        data=[((1,"OOP","2023-06-15T10:00:00.898000","2023-06-15T14:00:00.898000","link"))]
        expected=[Event.read_from_query_result(*data[0])]
        result=calendars.get_events_by_calendar_id(1,db)
        self.assertEqual(expected,result)
    
    def test_get_events_by_calendarIDNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=calendars.get_events_by_calendar_id(1,db)
        self.assertEqual(expected,result)
    
    def test_create_event_inCalendar(self):
        db=lambda q,event:1
        event=EventCreate(name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")
        expected=Event(id=1,name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")
        result=calendars.create_event_in_calendar(event,1,db)
        self.assertEqual(expected,result)
    
    def test_modify_eventName(self):
        db=lambda q,change:None
        expected=None
        change=EventChange(name="Java")
        result=calendars.modify_event(1,change,db)
        self.assertEqual(expected,result)
    
    def test_modify_eventStart(self):
        db=lambda q,change:None
        expected=None
        change=EventChange(start="2023-06-15T10:00:00.898000")
        result=calendars.modify_event(1,change,db)
        self.assertEqual(expected,result)
    
    def test_modify_eventEnd(self):
        db=lambda q,change:None
        expected=None
        change=EventChange(end="2023-06-15T10:00:00.898000")
        result=calendars.modify_event(1,change,db)
        self.assertEqual(expected,result)
    
    def test_modify_eventLinkToEvent(self):
        db=lambda q,change:None
        expected=None
        change=EventChange(link_to_event="link")
        result=calendars.modify_event(1,change,db)
        self.assertEqual(expected,result)     
    
    def test_delete_event(self):
        db=lambda q,id:None
        expected=None
        result=calendars.delete_event(1,db)
        self.assertEqual(expected,result)
    
    def test_modify_calendar(self):
        db=lambda q,calendar:None
        expected=None
        calendar=CalendarChange(owner_id=1)
        result=calendars.modify_calendar(1,calendar,db)
        self.assertEqual(expected,result)    
    
    def test_get_event_byIDWithData(self):
        db=lambda q,id:[(1,"OOP","2023-06-15T10:00:00.898000","2023-06-15T14:00:00.898000","link")]
        data=[(1,"OOP","2023-06-15T10:00:00.898000","2023-06-15T14:00:00.898000","link")]
        expected=Event.read_from_query_result(*data[0])
        result=calendars.get_event_by_id(1,db)
        self.assertEqual(expected,result)     
