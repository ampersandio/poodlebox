import unittest
from unittest.mock import Mock
from api.services import calendars
from api.data.models import Calendar, Event, CalendarChange, CalendarById, CalendarCreate, EventChange, EventCreate, TeacherShow

mock_db=Mock()
calendars.database=mock_db

class CalendarServiceShould(unittest.TestCase):
    def test_get_all_calendars_studentsWithData(self):
        mock_db.read_query.return_value=[(1,2)]
        expected=[Calendar(id=1,name="Python",course_id=1,owner_id=1),Calendar(id=2,name="Java",course_id=2,owner_id=2)]
        result=calendars.get_all_calendars_students(3)
        self.assertEqual(expected,result)
    
    def test_get_all_calendars_studentsNoData(self):
        mock_db.read_query.return_value=[(None,)]
        expected=[]
        result=calendars.get_all_calendars_students(3)
        self.assertEqual(expected,result)
    
    def test_get_all_calendarsAdminWithData(self):
        mock_db.read_query.return_value=[(1,2)]
        expected=[Calendar(id=1,name="Python",course_id=1,owner_id=1),Calendar(id=2,name="Java",course_id=2,owner_id=2)]
        result=calendars.get_all_calendars_admin()
        self.assertEqual(expected,result)
    
    def test_get_all_calendarsAdminNoData(self):
        mock_db.read_query.return_value=[(None,)]
        expected=[]
        result=calendars.get_all_calendars_admin()
        self.assertEqual(expected,result)
           
    def test_get_all_calendarsTeacherWithData(self):
        mock_db.read_query.return_value=[(1,2)]
        expected=[Calendar(id=1,name="Python",course_id=1,owner_id=1),Calendar(id=2,name="Java",course_id=2,owner_id=1)]
        result=calendars.get_all_callendars_teacher(1)
        self.assertEqual(expected,result)
    
    def test_get_all_calendarsTeacherNoData(self):
        mock_db.read_query.return_value=[(None,)]
        expected=[]
        result=calendars.get_all_callendars_teacher(1)
        self.assertEqual(expected,result)

    def test_createCalendar(self):
        mock_db.insert_query.read_data=[(1,)]
        calendar=CalendarCreate(name="Python",course_id=1)
        expected=None
        result=calendars.create_calendar(calendar)
        self.assertEqual(expected,result)
    
    def test_get_calendar_byIdWithData(self):
        mock_db.read_query.return_value=[(1,"Python",1,1,"Blago","Aleksandrova","3874864873","blago@abv.bg","linkedin")]
        teacher=TeacherShow(id=1,first_name="Blago",last_name="Aleksandrova",email="blago@abv.bg",phone_number="3874864873",linked_in_profile="linkedin")
        events=[Event(id=1,name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")]
        expected=CalendarById(id=1,name="Python",course_id=1,owner=teacher,events=events)
        result=calendars.get_calendar_by_id(1)
        self.assertEqual(expected,result)
    
    def test_create_event_inCalendar(self):
        mock_db.insert_query.return_value=1
        event=EventCreate(name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")
        expected=Event(id=1,name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")
        result=calendars.create_event_in_calendar(event,1)
        self.assertEqual(expected,result)
    
    def test_modify_eventName(self):
        mock_db.update_query.return_value=None
        expected=None
        change=EventChange(name="Java")
        result=calendars.modify_event(1,change)
        self.assertEqual(expected,result)
    
    def test_modify_eventStart(self):
        mock_db.update_query.return_value=None
        expected=None
        change=EventChange(start="2023-06-15T10:00:00.898000")
        result=calendars.modify_event(1,change)
        self.assertEqual(expected,result)
    
    def test_modify_eventEnd(self):
        mock_db.update_query.return_value=None
        expected=None
        change=EventChange(end="2023-06-15T10:00:00.898000")
        result=calendars.modify_event(1,change)
        self.assertEqual(expected,result)
    
    def test_modify_eventLinkToEvent(self):
        mock_db.update_query.return_value=None
        expected=None
        change=EventChange(link_to_event="link")
        result=calendars.modify_event(1,change)
        self.assertEqual(expected,result)     
    
    def test_delete_event(self):
        mock_db.update_query.return_value=None
        expected=None
        result=calendars.delete_event(1)
        self.assertEqual(expected,result)
    
    def test_modify_calendar(self):
        mock_db.update_query.return_value=None
        expected=None
        calendar=CalendarChange(owner_id=1)
        result=calendars.modify_calendar(1,calendar)
        self.assertEqual(expected,result)    
    
    def test_get_event_byIDWithData(self):
        mock_db.read_query.return_value=[(1,"OOP","2023-06-15T10:00:00.898000","2023-06-15T14:00:00.898000","link")]
        expected=Event(id=1,name="OOP",start="2023-06-15T10:00:00.898000",end="2023-06-15T14:00:00.898000",link_to_event="link")
        result=calendars.get_event_by_id(1)
        self.assertEqual(expected,result)     
