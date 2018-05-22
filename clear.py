"""
    read.py by Wilka Carvalho
    This function loads events from your google calendar between two times.
    It then creates on object with a list of dates, and each date contains information about the events on that date. E.g.,
    {'days': [{'date': '5/22',
           'day': 1,
           'events': [{'calendar': 'cal1',
                       'summary': 'watch',
                       'time': '04:00'},
                      {'calendar': 'cal2',
                       'summary': 'read',
                       'time': '18:00'}]},
          {'date': '5/24',
           'day': 3,
           'events': [{'calendar': 'cal2',
                       'summary': 'read',
                       'time': '18:00'}]}
    }
    This is either printed out or saved to a yaml file. 
"""
# python utils
import yaml
import pprint
import argparse

# Google
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# date utilities
from pytz import timezone
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime, timedelta

# this library
from lib import get_calendars_info, setup_calendar, load_start_end
from read import load_events, display_events, read_google_event_time

def delete_events(service, calendars, all_events, absolute_start, timezone, verbose=False):
  for cal in calendars:
    events = all_events[cal]
    if verbose and events:
      print()
      print(cal)
    for event in events:
        start, _ = read_google_event_time(event)
        start = start.astimezone(timezone)
        if start < absolute_start: continue
        if verbose:
          print("Deleting %d/%d/%d %.2d:%.2d %s" %(start.month, start.day, start.year, start.hour, start.minute, event['summary']))
        service.events().delete(calendarId=calendars[cal]['id'], eventId=event['id']).execute()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
  parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  args = parser.parse_args()

  tzinfo = tz.gettz(args.timezone)
  if not args.start:
      raise RuntimeError("Please select a day to clear")
  start, end = load_start_end(args.start, args.end, tzinfo)

  service = setup_calendar()
  calendars = get_calendars_info(service)
  all_events = load_events(service, calendars, start, end)
  delete_events(service, calendars, all_events, start, tzinfo, args.verbose)

if __name__ == "__main__":
    main()
