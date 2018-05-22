"""
    put.py by Wilka Carvalho
    This function loads events from a yaml file and places them on your google calendar starting on the date of your choice.
"""

# python utils
import yaml
import pprint
import argparse

# date utilities
from pytz import timezone
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

# this library
from lib import get_calendars_info, setup_calendar



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default=None, help="yaml file to load data from.")
parser.add_argument("-r", "--repeat", default=0, help="How often to repeat. E.g., every 1 day, 7 days, etc. If put 0, will not repeat.")
parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current date.")
# parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
parser.add_argument("-t", "--timezone", default="US/Pacific")
# parser.add_argument("-v", "--verbose", action='store_true')
args = parser.parse_args()

file=args.file
if not file:
  raise RuntimeError("Please provide a file to load from.")
f = open(file, 'r'); 
data={}
data.update(yaml.load(f))

tz = timezone(args.timezone)
format = "%m/%d/%Y"
if args.start: 
    start = datetime.strptime(args.start, format).replace(tzinfo=tz).replace(hour=0,minute=0)
else: 
    start = datetime.now(tz=tz).replace(hour=0,minute=0)

service = setup_calendar()
calendars = get_calendars_info(service)

cur_time = start.replace()
starting_day = data['days'][0]['day']
for day in data['days']:
  for event in day['events']:

    # get start hour + minute
    hour, minute = [int(i) for i in event['time'].split(":")]
    event_time = cur_time.replace(hour=hour, minute=minute)

    event_json = {
      'summary': event['summary'],
      'start': {
        'dateTime': str(event_time.isoformat()),
        'timeZone': args.timezone,
      },
      'end': {
        'dateTime': str((event_time + timedelta(minutes=event['length'])).isoformat()),
        'timeZone': args.timezone,
      }
    }

    # pprint.pprint(event_json)
    # calendarId = calendars[event['calendar']]['id']
    # event = service.events().insert(calendarId=calendarId, body=event_json).execute()
  break

# pprint.pprint(data)
# 
