"""Summary

Attributes:
    term (TYPE): Description
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
# from termcolor import colored
import collections
from tabulate import tabulate
from blessed import Terminal
import yaml

# date utilities
from dateutil.parser import parse
from dateutil import tz

# this library
from calendar_automator.lib import get_calendar_dicts, load_calendar_service, load_start_end, flatten_events
from calendar_automator.read import load_events
from calendar_automator.clear import clear_events



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. default: current time.")
    parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. default: end of current day.")
    parser.add_argument("--clear", default=1, type=int, help="whether to clear everything from target")
    parser.add_argument("--verbose", default=1, type=int, help="verbosity")
    parser.add_argument("--source", default=None, nargs="+", help="calendars to load data from")
    parser.add_argument("--target", default=None, nargs="+", help="calendars to load data from")
    parser.add_argument("-t", "--timezone", default="US/Eastern", help="default: US/Eastern")
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
    start, end = load_start_end(args.start, args.end, tzinfo)


    # ======================================================
    # load calendars
    # ======================================================
    calendar_service = load_calendar_service(
        credentials=os.path.join(parent_dir_path, settings['credentials']),
        )

    source_calendar_names = args.source or settings['calendars']
    assert source_calendar_names is not None and args.target is not None, "set source and target"
    source_calendars = get_calendar_dicts(calendar_service, 
        calendar_names=source_calendar_names)
    target_calendars = get_calendar_dicts(calendar_service, 
        calendar_names=args.target)

    # ======================================================
    # clear events in target
    # ======================================================
    if args.clear:
        # if clear, remove all events in that range already
        clear_events(service=calendar_service, calendars=target_calendars, start=start, end=end, tzinfo=tzinfo, verbose=args.verbose)


    # ======================================================
    # get all source events
    # ======================================================
    calendar2event = load_events(calendar_service, source_calendars, start, end, tzinfo) # per calendar
    source_events = flatten_events(calendar2event, sort=False)

    # ======================================================
    # copy to target
    # ======================================================
    assert len(target_calendars) == 1
    target_id = target_calendars[args.target[0]]['id']
    keys = ['summary', 'end', 'start']
    for event in source_events:
        body = {k:event[k] for k in keys}
        calendar_service.events().insert(calendarId=target_id, body=body).execute()
        # if args.verbose:
        #   print("Added %d/%d/%d %.2d:%.2d %s" %(start.month, start.day, start.year, start.hour, start.minute, event['summary']))

if __name__ == '__main__':
  main()