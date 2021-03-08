import os
# from apiclient.discovery import build
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pickle
from httplib2 import Http
from oauth2client import file, client, tools

from dateutil.parser import parse
from datetime import datetime, timedelta
import yaml


def apply_to_events(events, fn, *args, **kwargs):
  for event in events:
    fn(*([event] + list(args)), **kwargs)

def read_google_event_time(event):
  # ev_start = event['start'].get('dateTime', event['start'].get('date'))
  start = event['start'].get('dateTime', event['start'].get('date'))
  end = event['end'].get('dateTime', event['end'].get('date'))
  return parse(start), parse(end)

def load_yaml(file):
  # load data from file
  if not file:
    raise RuntimeError("Please provide a file to load from.")
  f = open(file, 'r'); 
  data={}
  data.update(yaml.load(f))
  return data

def flatten_events(events_calendar_dic, sort=False):
  """Take a dictionary of that maps calendar name to events and return a long list of all the events. the events are themselves dics and will now have an entry that maps to the calendar name
  """

  events = []
  for calendar, events_list in events_calendar_dic.items():
    for event in events_list:
      event['calendar'] = calendar
    events += events_list

  if sort: return sorted(events, key = lambda x: parse(x['start']['dateTime']))
  return events





# ======================================================
# loading calendars
# ======================================================
def load_calendar_service(credentials="credentials.json"):
    """Summary

    Args:
      credentials (str, optional): Description
      secret (str, optional): Description

    Returns:
      TYPE: Description
    """
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    creds = None

    path = os.path.dirname(os.path.abspath(credentials))
    token_file = os.path.join(path, 'token.pickle')

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # store = file.Storage(credentials)
    # creds = store.get()
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    # return build('calendar', 'v3', http=creds.authorize(Http()))
    service = build('calendar', 'v3', credentials=creds)

    return service


def get_calendar_dicts(service, calendar_names, desired_attributes = ['id']):
  """Summary
  
  Args:
      service (TYPE): Description
      calendar_names (TYPE): Description
      desired_attributes (list, optional): Description
  
  Returns:
      TYPE: Description
  """
  calendar_dicts = {c: {} for c in calendar_names}
  
  page_token = None
  while True:
    google_calendars = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in google_calendars['items']:
      key=calendar_list_entry['summary'].lower()
      if key in calendar_names:
          for att in desired_attributes:
              calendar_dicts[key][att] = calendar_list_entry[att]
      # else:
      #   print(f"Skipped: {key}")

    # import ipdb; ipdb.set_trace()
    page_token = google_calendars.get('nextPageToken')
    if not page_token:
      break


  return calendar_dicts

# def load_calendars_from_file(file="calendars.yaml", op='planning'):
#   stream = open(file, 'r')
#   dic = next(yaml.load_all(stream))
#   return [i for i in dic[op]]



# ======================================================
# Misc.
# ======================================================

def load_start_end(start, end, tzinfo):
  # tzinfo info:
  # replace: keeps current time and uses timezone
  # astimezone: converts time to that timezone
  if start: 
    start = parse(start).replace(tzinfo=tzinfo)
  else: 
    start = datetime.now(tz=tzinfo)
  if end: 
    # inclusive of current date
    end = parse(end).replace(tzinfo=tzinfo)
  else:
    end = start + timedelta(days=1)
    end = parse(str(end.date())).replace(tzinfo=tzinfo)

  if end <= start:
    print(start)
    print(end)
    raise RuntimeError("end must be later than start")
  return start, end
