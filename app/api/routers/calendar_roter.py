import requests
import json
from fastapi import APIRouter, Request, Header, Depends, Response, HTTPException
from api.data.models import User, Query, Calendar, Event, Rule
from api.services.authorization import get_current_user
from starlette.datastructures import URL, Headers
from fastapi_pagination import paginate, Page
from typing import Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pickle
from googleapiclient.errors import Error

from api.services.authorization import start_service
import json

calendar_router=APIRouter(prefix="/calendars",tags=["Google Calendars"])

SCOPES = ['https://www.googleapis.com/auth/calendar']



@calendar_router.post("/login")
def login():
    try:
     flow = InstalledAppFlow.from_client_secrets_file("api/utils/client_secret.json", SCOPES)
     creds=flow.run_local_server()

     pickle.dump(creds, open("token.pkl", "wb"))
     credentials = pickle.load(open("token.pkl", "rb"))
     return credentials
    except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
        raise HTTPException(status_code=400, detail=json.loads(e.content))



@calendar_router.get("/")
def get_all_calendars(service=Depends(start_service)):
    try:
     result=service.calendarList().list().execute()
     return result
    except Error as e:
      if hasattr(e,'resp'):
        raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
       raise HTTPException(status_code=400, detail=json.loads(e.content))

  


@calendar_router.post("/")
def create_calendars(calendar:Calendar,service=Depends(start_service)):
 try:
   new_calendar={"summary":calendar.summary}
   service.calendars().insert(body=new_calendar).execute()
   result = service.calendarList().list().execute()

   return result['items']
 except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
       raise HTTPException(status_code=400, detail=json.loads(e.content))

  
@calendar_router.get("/{calendar_id}")
def get_calendar_by_calendar_id(calendar_id:str,service=Depends(start_service)):
   try:
    events=service.events().list(calendarId=calendar_id).execute()
    return events
   except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
       raise HTTPException(status_code=400, detail=json.loads(e.content))


@calendar_router.post("/{calendar_id}/events")
def create_event_in_calendars(calendar_id:str,event:Event,service=Depends(start_service)):
   try:
    body_event={"summary":event.summary,
               "start":{"dateTime":event.start["dateTime"],"timeZone":"UTC"},
               "end":{"dateTime":event.end['dateTime'],"timeZone":"UTC"}}
    service.events().insert(calendarId=calendar_id, body=body_event).execute()
    events=service.events().list(calendarId=calendar_id).execute()
    return events
   except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
       raise HTTPException(status_code=400, detail=json.loads(e.content))


@calendar_router.post("/{calendar_id}/users/calendars")
def add_calendar_to_users_list(calendar_id:str,service=Depends(start_service)):
   calendar_list_entry = {
    'id': calendar_id}
   try:
    created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry).execute()

    return created_calendar_list_entry['summary']
   except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
       raise HTTPException(status_code=400, detail=json.loads(e.content))


@calendar_router.post("/{calendar_id}/users")
def add_user_to_calendar(calendar_id:str,rule:Rule,service=Depends(start_service)):
    try:
     rule = {
    'scope': rule.scope,
    'role': rule.role
     }  
     created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()

     return created_rule
    except Error as e:
      if hasattr(e,'resp'):
       raise HTTPException(status_code=e.resp.status, detail=json.loads(e.content))
      else:
        raise HTTPException(status_code=400,detail=json.loads(e.content))
