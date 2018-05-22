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
    #       calculate day by difference (use datetime object??)
    data['days'] = sorted(data['days'], key = lambda x: x["date"])
    
    # sort events within days by time
    for day in data['days']:
        if len(day['events']) > 1:
            day['events'] = sorted(day['events'], 
                                   key = lambda x: x["time"])
    import ipdb; ipdb.set_trace()

    return data


def save_events(all_events, file):

    data = create_events_object(all_events)


# {'events': [{'date': '5/21',
#              'day': 1,
#              'events': [{'calendar': '1. urgent',
#                          'summary': 'read',
#                          'time': 1080},
#                         {'summary': 'block', 'time': 1410}]},
#             {'date': '5/22', 'day': 2}]}



    file = open(file, 'w')
            # file.write("%d/%d/%d %.2d:%.2d: %s\n" %(date.month, date.day, date.year, date.hour, date.minute, event['summary']))
            # ev_start = event['start'].get('dateTime', event['start'].get('date'))
            # print(ev_start, event['summary'])


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
    save_events(all_events, args.file)

# start = datetime(2018, 5, 17, 0, 0, 0, tzinfo=tz).isoformat()
# end = datetime(2018, 5, 17, 23, 30, 0, tzinfo=tz).isoformat()

# print(args)
# print(end)
# 