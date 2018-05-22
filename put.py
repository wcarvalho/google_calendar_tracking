"""
    put.py by Wilka Carvalho
    This function loads events from a yaml file and places them on your google calendar starting on the date of your choice.
"""

# python utils
import yaml
import pprint
import argparse

# date utilities
# from pytz import timezone
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil import tz
from datetime import datetime, timedelta

# this library
from lib import get_calendars_info, setup_calendar

def load_template(file):
  # load data from file
  if not file:
    raise RuntimeError("Please provide a file to load from.")
  f = open(file, 'r'); 
  data={}
  data.update(yaml.load(f))
  return data


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", default=None, help="yaml file to load data from.")
  parser.add_argument("-r", "--repeat", default=0, help="How often to repeat. E.g., every 1 day, 7 days, etc. If put 0, will not repeat.")
  parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current date.")
  # parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  args = parser.parse_args()

  data = load_template(args.file)

  tzinfo = tz.gettz(args.timezone)
  start, end = load_start_end(args.start, args.end, tzinfo)

  service = setup_calendar()
  calendars = get_calendars_info(service)

  starting_day = data['days'][0]['day']
  for day in data['days']:
    if args.verbose:
      print("Day %d" % day)
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
      calendarId = calendars[event['calendar']]['id']
      event = service.events().insert(calendarId=calendarId, body=event_json).execute()
      if args.verbose:
        print("%s %s: %s" % (str(event_time.date()), str(event_time.time()), event['summary']))
    break

  # pprint.pprint(data)
  # 


if __name__ == "__main__":
    main()
