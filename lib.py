from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from dateutil.parser import parse
from datetime import timedelta
import yaml

def load_yaml(file):
  # load data from file
  if not file:
    raise RuntimeError("Please provide a file to load from.")
  f = open(file, 'r'); 
  data={}
  data.update(yaml.load(f))
  return data

def load_start_end(start, end, tzinfo):
  # tzinfo info:
      # replace: keeps current time and uses timezone
      # astimezone: converts time to that timezone
  if start: 
    start = parse(start).replace(tzinfo=tzinfo)
  else: 
    start = datetime.now(tz=tzinfo)
  if end: 
    end = parse(end).replace(tzinfo=tzinfo)
  else:
    end= start + timedelta(days=1)
    end = parse(str(end.date())).replace(tzinfo=tzinfo)

  if end <= start:
    raise RuntimeError("end must be later than start")
  return start, end

def get_calendars_info(service, f="calendars.yaml", op='planning', desired_attributes = ['id']):
  stream = open(f, 'r')
  dic = next(yaml.load_all(stream))
  calendars = {p: {} for p in dic[op]}
  
  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      key=calendar_list_entry['summary'].lower()
      if key in dic[op]:
          for att in desired_attributes:
              calendars[key][att] = calendar_list_entry[att]
    page_token = calendar_list.get('nextPageToken')
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

