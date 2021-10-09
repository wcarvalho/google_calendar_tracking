"""
    clear.py by Wilka Carvalho
"""
# get path of file
import sys
import os
from pprint import pprint
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))

# change path to settings
SETTINGS_FILEPATH=os.path.join(parent_dir_path, "settings.yaml")




# python utils
import argparse

# Google

# date utilities
from dateutil import tz

# this library
from calendar_automator.lib import apply_to_events, flatten_events, load_calendar_service
from calendar_automator.read import load_events, read_google_event_time

def clear_event(event, service, calendars, tzinfo, test_only=False, verbose=True):
        start, _ = read_google_event_time(event)
        start = start.astimezone(tzinfo)
        if not test_only:
          cal_id = calendars[event['calendar']]['id']
          service.events().delete(calendarId=cal_id, eventId=event['id']).execute()
        if verbose:
          print("Deleting %d/%d/%d %.2d:%.2d %s" %(start.month, start.day, start.year, start.hour, start.minute, event['summary']))

def clear_events(service, calendars, start, end, tzinfo, test_only=False, verbose=False):
  all_events = load_events(service, calendars, start, end, tzinfo)
  sorted_events = flatten_events(all_events, sort=True)
  apply_to_events(sorted_events, clear_event, service, calendars, tzinfo, test_only, verbose)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
  parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  parser.add_argument("-T", "--test-only", action='store_true')
  args = parser.parse_args()

  tzinfo = tz.gettz(args.timezone)

  # ======================================================
  # load settings
  # ======================================================
  with open(SETTINGS_FILEPATH, 'r') as f:
    settings = yaml.safe_load(f)

  # ======================================================
  # parse start and end dates into objects
  # ======================================================
  if not args.start:
      raise RuntimeError("Please select a day to clear")
  start, end = load_start_end(args.start, args.end, tzinfo)

  # ======================================================
  # load claendars
  # ======================================================
  calendar_service = load_calendar_service(
    credentials=os.path.join(parent_dir_path, settings['credentials']),
    )
  calendar_names = args.calendars or settings['calendars']
  calendars = get_calendar_dicts(calendar_service, 
    calendar_names=calendar_names)

  clear_events(calendar_service, calendars, start, end, tzinfo, args.test_only, args.verbose)

if __name__ == "__main__":
    main()