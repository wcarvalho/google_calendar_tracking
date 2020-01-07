"""
    shift.py by Wilka Carvalho 
"""
# python utils
import argparse

# date utilities
from dateutil import tz
from datetime import timedelta

# this library
from calendar_automator.lib import *
from calendar_automator.read import load_events, read_google_event_time

def shift(event, service, calendars, tzinfo, minutes, test_only, verbose):
    start, end = read_google_event_time(event)
    start = start.astimezone(tzinfo) + timedelta(minutes=minutes)
    end = end.astimezone(tzinfo) + timedelta(minutes=minutes)

    event['start']['dateTime'] = str(start.isoformat())
    event['end']['dateTime'] = str(end.isoformat())

    cal_id = calendars[event['calendar']]['id']

    if not test_only:
        updated_event = service.events().update(calendarId=cal_id, eventId=event['id'], body=event).execute()
    if verbose:
        print("%s %s: %s" % (str(start.date()), str(start.time()), event['summary']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None, help="if set, will save to this file. currently only support yaml.")
    parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
    parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
    parser.add_argument("-t", "--timezone", default="US/Pacific")
    parser.add_argument("-m", "--minutes", type=int, default=0)
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-T", "--test-only", action='store_true')
    args = parser.parse_args()

    tzinfo = tz.gettz(args.timezone)
    if not (args.start):
      raise RuntimeError("Please select a time-period beginning to shift")
    start, end = load_start_end(args.start, args.end, tzinfo)

    service = setup_calendar()
    calendar_list = load_calendars_from_file()
    calendars = get_calendars_info(service, calendar_list)

    all_events = load_events(service, calendars, start, end, tzinfo)
    all_events = flatten_events(all_events, sort=True)
    apply_to_events(all_events, shift, service, calendars, tzinfo, args.minutes, args.test_only, args.verbose)
    
if __name__ == "__main__":
    main()
