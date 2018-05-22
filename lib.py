from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import yaml

def get_calendars_info(service, f="calendars.yaml", op='planning', desired_attributes = ['id']):
  stream = open(f, 'r')
  dic = next(yaml.load_all(stream))
  calendars = {p: {} for p in dic[op]}
  
  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      if calendar_list_entry['summary'] in dic[op]:
          for att in desired_attributes:
              calendars[calendar_list_entry['summary']][att] = calendar_list_entry[att]
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break
  return calendars

def setup_calendar(credentials="credentials.json", secret="client_secret.json"):
  SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
  store = file.Storage(credentials)
  creds = store.get()
  if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets(secret, SCOPES)
      creds = tools.run_flow(flow, store)
  return build('calendar', 'v3', http=creds.authorize(Http()))

