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
from calendar_automator.lib import get_calendars_info, setup_calendar, load_start_end, load_yaml, load_calendars_from_file
from clear import clear_events

def put_events(data, calendars, service, start, timezone, verbose=False, test_only=False):

  starting_day = data['days'][0]['day']
  for day in data['days']:
    if verbose:
      print("Day %d" % day['day'])

    cur_time = start + timedelta(days=day['day']-starting_day)

    for event in day['events']:

      # get start hour + minute
      hour, minute = [int(i) for i in event['time'].split(":")]
      event_time = cur_time.replace(hour=hour, minute=minute)

      if not test_only:
        event_json = {
          'summary': event['summary'],
          'start': {
            'dateTime': str(event_time.isoformat()),
            'timeZone': timezone,
          },
          'end': {
            'dateTime': str((event_time + timedelta(minutes=event['length'])).isoformat()),
            'timeZone': timezone,
          }
        }
        calendarId = calendars[event['calendar']]['id']
        event = service.events().insert(calendarId=calendarId, body=event_json).execute()
      if verbose:
        print("%s %s: %s" % (str(event_time.date()), str(event_time.time()), event['summary']))


def tile(data, calendars, service, start, end, timezone, repeat=None, verbose=False, test_only=False):
  # import ipdb; ipdb.set_trace()
  day_1 = data['days'][0]['day']
  day_n = data['days'][-1]['day']
  template_length = day_n - day_1

  # if don't define repetition, will tile one longer than template length
  if not repeat: repeat = template_length + 1
  
  if repeat <= template_length: 
    raise RuntimeError(
      """
      Your repeat frequency and your template length overlap.
      E.g., If end day is 7 (e.g. Sunday) and start day is 1 (e.g. Monday)
      then the minimum repeat time is 7 > (7-1). Anything less, and there's overlap.
      """
      )
  end_date = start + timedelta(days=template_length)
  indx = 0
  while (True):
    # get start date & end_date
    start = start + timedelta(days=repeat if indx else indx)
    end_date = start + timedelta(days=template_length)
    if end_date >= end:
      if verbose:
        print("Finished on %s - %s " % (str(start.date()), str(end_date.date())))
        if not indx: 
          print("Didn't repeat. Maybe change your end date to some further in the future?")
      break
    # if end_date is before end, place events
    if verbose:
      print()
      print("Instance %d: %s - %s" % (indx, str(start.date()), str(end_date.date())))
    put_events(data, calendars, service, start, timezone, verbose,test_only)

    indx += 1

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", default=None, help="yaml file to load data from.")
  parser.add_argument("-r", "--repeat", default=0, type=int, help="How often to repeat. E.g., every 1 day, 7 days, etc. If put 0, will not repeat.")
  parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current date.")
  parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  parser.add_argument("-c", "--clear", action='store_true')
  parser.add_argument("-T", "--test-only", action='store_true')
  args = parser.parse_args()

  data = load_yaml(args.file)

  tzinfo = tz.gettz(args.timezone)
  start, end = load_start_end(args.start, args.end, tzinfo)

  service = setup_calendar()
  calendar_list = load_calendars_from_file()
  calendars = get_calendars_info(service, calendar_list)

  if args.clear:
    # if clear, remove all events in that range already
    clear_events(service, calendars, start, end, tzinfo, args.verbose)

  if args.repeat:
    tile(data, calendars, service, start, end, args.timezone, args.repeat, args.verbose, args.test_only)
  else:
    put_events(data, calendars, service, start, args.timezone, args.verbose, args.test_only)


if __name__ == "__main__":
    main()

