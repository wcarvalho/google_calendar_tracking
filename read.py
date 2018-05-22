from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pytz import timezone
from dateutil.parser import parse
import pytz

from datetime import datetime, timedelta
import yaml
import pprint
import argparse



from lib import get_calendars_info, setup_calendar

def read_google_event_time(event):
    # ev_start = event['start'].get('dateTime', event['start'].get('date'))
    time = event['start'].get('dateTime')
    return parse(time)

def load_events(service, calendars, start, end, maxResults=1000):
    events = {}
    for cal in calendars:
        id = calendars[cal]['id']
        events_result = service.events().list(
            calendarId=id,
            timeMin=start, 
            timeMax=end,
            maxResults=maxResults, singleEvents=True,
            orderBy='startTime').execute()
        events[cal] = events_result.get('items', [])
    return events

def display_events(all_events):
    for cal in calendars:
        events = all_events[cal]

        print()
        print(cal)
        if not events:
            print('No upcoming events found.')
        for event in events:
            date = read_google_event_time(event)

            print("%d/%d/%d %.2d:%.2d" %(date.month, date.day, date.year, date.hour, date.minute), event['summary'])

def create_events_object(all_events):

    data = {"days":[]}
    pointers = {}

    for cal in calendars:
        events = all_events[cal]

        for event in events:
            date = read_google_event_time(event)

            # keep pointers to elements which are accessed by the date
            key = "%d/%d/%d" % (date.month, date.day, date.year)
            if key in pointers:
                element = pointers[key]
            else:
                element = {}
                pointers[key] = element
                data["days"].append(element)

            # element["day"] = day
            element["raw"] = str(date)
            element["date"] = "%d/%d" %(date.month, date.day)
            event_info = {
                "summary": event["summary"],
                "time": "%.2d:%.2d" %(date.hour, date.minute),
                "calendar": cal
                    }
            if "events" in element:
                element["events"].append(event_info)
            else:
                element["events"] = [event_info]

    # sort days by dates
    data['days'] = sorted(data['days'], key = lambda x: x["date"])
    
    # sort events within days by time
    for day in data['days']:
        if len(day['events']) > 1:
            day['events'] = sorted(day['events'], 
                                   key = lambda x: x["time"])
    
    data['days'][0]['day'] = 1; 
    # if only 1 date, set day and return. else calculate difference
    if len(data['days']) == 0:
        return data
    
    # calculate days by day-differences useing datetime objects via parse
    day0 = data['days'][0]
    for day1 in data['days'][1:]:
        # get datetime objects starting at midnight
        date0 = parse(day0['raw']).replace(hour=0,minute=0)
        date1 = parse(day1['raw']).replace(hour=0,minute=0)
        # get difference in number of days
        day_difference = date1-date0
        day_difference = day_difference.days
        # update 2nd date
        day1['day'] = day0['day'] + day_difference
        # update 1st element for loop
        day0=day1

    return data


def save_events(data, file):
    file = open(file, 'w')
    yaml.dump(data, file)


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default=None, help="if set, will save to this file. currently only support yaml.")
parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
parser.add_argument("-t", "--timezone", default="US/Pacific")
parser.add_argument("-v", "--verbose", action='store_true')
args = parser.parse_args()

tz = timezone(args.timezone)

format = "%m/%d/%Y %H:%M"

if args.start: 
    start = datetime.strptime(args.start, format).replace(tzinfo=tz).isoformat()
else: 
    start = datetime.now(tz=tz).isoformat()
if args.end: 
    end = datetime.strptime(args.end, format).replace(tzinfo=tz).isoformat()
else:
    raise RuntimeError("Not yet implemented when don't set `--end`")

service = setup_calendar()
calendars = get_calendars_info(service)
all_events = load_events(service, calendars, start, end)

if args.verbose: display_events(all_events)
if args.file:
    data = create_events_object(all_events)
    save_events(data, args.file)