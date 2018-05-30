from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from dateutil.parser import parse
from datetime import datetime, timedelta
import yaml

def load_yaml(file):
  # load data from file
  if not file:
    raise RuntimeError("Please provide a file to load from.")
  f = open(file, 'r'); 
  data={}
  data.update(yaml.load(f))
  return data

def flatten_events(events_calendar_dic):
    """Take a dictionary of that maps calendar name to events and return a long list of all the events. the events are themselves dics and will now have an entry that maps to the calendar name
    """

    events = []
    for calendar, events_list in events_calendar_dic.items():
      for event in events_list:
        event['calendar'] = calendar
      events += events_list

    return events




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
    end = parse(end).replace(tzinfo=tzinfo) + timedelta(days=1)
  else:
    end= start + timedelta(days=1)
    end = parse(str(end.date())).replace(tzinfo=tzinfo)

  if end <= start:
    raise RuntimeError("end must be later than start")
  return start, end

def load_calendars_from_file(f="calendars.yaml", op='planning'):
  stream = open(f, 'r')
  dic = next(yaml.load_all(stream))
  return [i for i in dic[op]]

def get_calendars_info(service, calendar_names, desired_attributes = ['id']):
  calendars = {c: {} for c in calendar_names}
  
  page_token = None
  while True:
    google_calendars = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in google_calendars['items']:
      key=calendar_list_entry['summary'].lower()
      if key in calendar_names:
          for att in desired_attributes:
              calendars[key][att] = calendar_list_entry[att]
    page_token = google_calendars.get('nextPageToken')
    if not page_token:
      break
  return calendars

def setup_calendar(credentials="credentials.json", secret="client_secret.json"):
  SCOPES = 'https://www.googleapis.com/auth/calendar'
  store = file.Storage(credentials)
  creds = store.get()
  if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets(secret, SCOPES)
      creds = tools.run_flow(flow, store)
  return build('calendar', 'v3', http=creds.authorize(Http()))

