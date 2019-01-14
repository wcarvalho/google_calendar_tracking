"""
    available_time.py by Wilka Carvalho
"""
# python utils
import yaml
from pprint import pprint
import argparse
from termcolor import colored
# import hashlib


# date utilities
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime, timedelta

# this library
from lib import get_calendars_info, setup_calendar, load_start_end, load_yaml, flatten_events, load_calendars_from_file
from read import load_events


colors = ["red", "green", "yellow", "magenta", "cyan"]

def calculate_time_scheduled(events, raw_end, end, tzinfo):
  # for task in tasks:
  #   if not 'end' in task: 
  #     if 'start' in task:
  #       task['end'] = parse(task['start']).replace(tzinfo=tzinfo)
  #       task['end'] = task['end'] if task['end'] > end else end
  #     else:
  #       task['end'] = end

  # tasks = sorted(tasks, key = lambda x: x['end'])

  # turn start dateTime into a datetime object for all events
  for event in events:
    event['start']['dateTime'] = parse(event['start']['dateTime'])
  # turn events into an iterable to query
  events = sorted(events, key = lambda x: x['start']['dateTime'])

  nevents = len(events)

  def split_category_activity(string):
    split = string.split(":")
    # print(split)
    # if len(split) > 2:
    #   import ipdb; ipdb.set_trace()
    if len(split) == 1:
      return split[0], split[0]
    elif len(split) == 2:
      return split
    elif len(split) == 0:
      raise RuntimeError("empty string?")
    else:
      return split[0], " : ".join(split[1:])

  tasks = {}
  total_time = 0
  for event in events:
    summary = event['summary']
    event_start = event['start']['dateTime'].replace(tzinfo=tzinfo)
    event_end = parse(event['end']['dateTime']).replace(tzinfo=tzinfo)
    dif = event_end - event_start
    minutes = dif.total_seconds()/60
    total_time += minutes

    category, activity = split_category_activity(summary)
    if category in tasks:
      if activity in tasks[category]:
        tasks[category][activity] += minutes
      else:
        tasks[category][activity] = minutes
    else:
      tasks[category] = {};
      tasks[category][activity] = minutes

  print("Total Time before %s: %2.2f" % (raw_end, total_time/60))
  # print("Total Time before %s/%s/%s: %2.2f" % (end.month, end.day, end.year, total_time/60))
  try: print("Total Unscheduled: %2.2f" % (tasks['block']['block']/60))
  except: pass

  for color_indx, category in enumerate(sorted(tasks.keys())):
    if category == 'block': continue
    total_per_category = 0
    for indx, activity in enumerate(tasks[category]):
      minutes = tasks[category][activity]
      total_per_category += minutes

    color_indx = (color_indx - 1)%len(colors)

    if len(tasks[category]) == 1:
      key = [i for i in tasks[category].keys()][0]
      print()
      if category == key:
        print("%s: %2.2f" % (key, total_per_category/60))
      else:
        print("%s.%s: %2.2f" % (colored(category, colors[color_indx]), key, total_per_category/60))
      continue

    print()
    print("%s: %2.2f" % (colored(category, colors[color_indx]), total_per_category/60))
    for indx, activity in enumerate(tasks[category]):
      minutes = tasks[category][activity]
      # print("\t%d. %s: %2.2fm/%2.2fh" % (indx+1, activity, minutes, minutes/60))
      print("\t%d. %s: %2.2fh" % (indx+1, activity, minutes/60))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None, help="yaml file to load task data from.")
    parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
    parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
    parser.add_argument("-t", "--timezone", default="US/Pacific")
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args()

    tzinfo = tz.gettz(args.timezone)

    # task_data = load_yaml(args.file)
    # tasks = flatten_tasks(task_data)

    service = setup_calendar()
    calendar_list = load_calendars_from_file()
    calendars = get_calendars_info(service, calendar_list)

    start, end = load_start_end(args.start, args.end, tzinfo)
    all_events = load_events(service, calendars, start, end, tzinfo)
    
    combined_events = []
    for calendar in calendars:
      combined_events += all_events[calendar]

    calculate_time_scheduled(combined_events, args.end, end, tzinfo)


if __name__ == '__main__':
  main()