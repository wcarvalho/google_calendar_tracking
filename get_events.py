from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pytz import timezone

import pytz

from datetime import datetime, timedelta
import yaml
import pprint
import argparse

from lib import get_calendars_info, setup_calendar

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", default=None)
parser.add_argument("-e", "--end", default=None)
parser.add_argument("-t", "--timezone", default="US/Pacific")
args = parser.parse_args()

tz = timezone(args.timezone)

format = "%m/%d/%Y %H:%M"

if not args.start: start = datetime.now(tz=tz).isoformat()
end = datetime.strptime(args.end, format).replace(tzinfo=tz).isoformat()

service = setup_calendar()
calendars = get_calendars_info(service)

pprint.pprint(calendars)

for cal in calendars:
    print()
    print(cal)
    id=calendars[cal]['id']
    events_result = service.events().list(
        calendarId=id, 
        timeMin=start, 
        timeMax=end,
        maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        ev_start = event['start'].get('dateTime', event['start'].get('date'))
        print(ev_start, event['summary'])

# start = datetime(2018, 5, 17, 0, 0, 0, tzinfo=tz).isoformat()
# end = datetime(2018, 5, 17, 23, 30, 0, tzinfo=tz).isoformat()

# print(args)
# print(end)
# 