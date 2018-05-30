"""
    put.py by Wilka Carvalho
    This function replicates a set of events
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
from lib import get_calendars_info, setup_calendar, load_start_end, load_yaml, load_calendars_from_file
from read import load_events, create_events_object
from clear import delete_events

def main():
  parser = argparse.ArgumentParser()
  # parser.add_argument("-f", "--file", default=None, help="yaml file to save data from.")
  parser.add_argument("-r", "--repeat", default=0, type=int, help="How often to repeat. E.g., every 1 day, 7 days, etc. If put 0, will not repeat.")
  parser.add_argument("-bR", "--base-range", default=None, nargs=2, help="start and end dates to load data from. format: month/day/year e.g. `-R 5/20/2018 5/24/2018`")
  parser.add_argument("-rR", "--repeat-range", default=None, nargs=2, help="start and end dates to to tile inside. format: month/day/year e.g. `-R 5/20/2018 5/24/2018`")
  parser.add_argument("-t", "--timezone", default="US/Pacific")
  parser.add_argument("-v", "--verbose", action='store_true')
  parser.add_argument("-c", "--clear", action='store_true')
  parser.add_argument("-T", "--test-only", action='store_true')
  args = parser.parse_args()

  tzinfo = tz.gettz(args.timezone)
  service = setup_calendar()
  calendar_list = load_calendars_from_file()
  calendars = get_calendars_info(service, calendar_list)

  # get the events to replicate in desired date range
  base_start, base_end = load_start_end(args.base_range[0], args.base_range[1], tzinfo)
  all_events = load_events(service, calendars, base_start, base_end)

  # create event object data to tile
  data = create_events_object(calendars, all_events, base_start, tzinfo)

  # get start and end dates for tiling
  repeat_start, repeat_end = load_start_end(args.repeat_range[0], args.repeat_range[1], tzinfo)

  if args.clear:
    # if clear, remove all events in that range already
    clear_events = load_events(service, calendars, repeat_start, repeat_end)
    delete_events(service, calendars, clear_events, repeat_start, tzinfo, args.verbose)
  
  tile(data, calendars, service, repeat_start, repeat_end, args.timezone, args.repeat, args.verbose, args.test_only)


if __name__ == "__main__":
    main()
