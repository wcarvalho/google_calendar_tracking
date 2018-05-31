"""
    clear.py by Wilka Carvalho

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

def clear_events(service, calendars, start, end, tzinfo, verbose):
  all_events = load_events(service, calendars, start, end)
  delete_events(service, calendars, all_events, start, tzinfo, verbose)

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
  calendar_list = load_calendars_from_file()
  calendars = get_calendars_info(service, calendar_list)
  clear_events(service, calendars, start, end, tzinfo, args.verbose)

if __name__ == "__main__":
    main()
