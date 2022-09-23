from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta

SCOPES = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/calendar.events","https://www.googleapis.com/auth/calendar.events.readonly","https://www.googleapis.com/auth/calendar.readonly"]
SUBJECT = os.environ['COMPANY_EMAIL']

events = []

credentials = service_account.Credentials.from_service_account_file("service_account_credentials.json", scopes=SCOPES)

delegated_credentials = credentials.with_subject(SUBJECT)
service = build('calendar', 'v3', credentials=delegated_credentials)

now = datetime.utcnow()
startDate = (now - relativedelta(months=1)).isoformat() + 'Z' # 'Z' indicates UTC time
endDate = (now + relativedelta(months=2)).isoformat() + 'Z'

def getEvents(pageToken: str) -> list:
  newEvents = service.events().list(calendarId=os.environ['CALENDAR_ID'],timeMin=startDate,maxResults=2000,timeMax=endDate,orderBy='startTime',pageToken=pageToken, singleEvents=True).execute()
  newEventsItems = newEvents['items']

  if "nextPageToken" in newEvents:
    newEventsItems = [*newEventsItems, *getEvents(newEvents['nextPageToken'])]
  
  return newEventsItems