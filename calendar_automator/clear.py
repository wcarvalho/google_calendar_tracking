"""
    clear.py by Wilka Carvalho

"""
# python utils
import argparse

# Google

# date utilities
from dateutil import tz

# this library
from calendar_automator.lib import *
from calendar_automator.read import load_events, read_google_event_time

# def delete_events(service, calendars, all_events, absolute_start, timezone, verbose=False):
#   for cal in calendars:
#     events = all_events[cal]
#     if verbose and events:
#       print()
#       print(cal)
#     for event in events:
#         if start < absolute_start: continue

def clear_event(event, service, calendars, tzinfo, test_only=False, verbose=True):
        start, _ = read_google_event_time(event)
        start = start.astimezone(tzinfo)
        if not test_only:
          cal_id = calendars[event['calendar']]['id']
          service.events().delete(calendarId=cal_id, eventId=event['id']).execute()
        if verbose:
          print("Deleting %d/%d/%d %.2d:%.2d %s" %(start.month, start.day, start.year, start.hour, start.minute, event['summary']))

def clear_events(service, calendars, start, end, tzinfo, test_only, verbose):
  all_events = load_events(service, calendars, start, end, tzinfo)
  sorted_events = flatten_events(all_events, sort=True)
  apply_to_events(sorted_events, clear_event, service, calendars, tzinfo, test_only, verbose)
  # delete_events(service, calendars, all_events, start, tzinfo, verbose)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
  parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  parser.add_argument("-T", "--test-only", action='store_true')
  args = parser.parse_args()

  tzinfo = tz.gettz(args.timezone)
  if not args.start:
      raise RuntimeError("Please select a day to clear")
  start, end = load_start_end(args.start, args.end, tzinfo)

  service = setup_calendar()
  calendar_list = load_calendars_from_file()
  calendars = get_calendars_info(service, calendar_list)
  clear_events(service, calendars, start, end, tzinfo, args.test_only, args.verbose)

if __name__ == "__main__":
    main()
