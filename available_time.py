"""
    available_time.py by Wilka Carvalho
"""
# python utils
import yaml
from pprint import pprint
import argparse

# date utilities
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime, timedelta

# this library
from lib import get_calendars_info, setup_calendar, load_start_end, load_yaml
from read import load_events

def flatten_tasks(task_data):
  tasks = []
  for category in task_data:
    for task in task_data[category]:
      task['category'] = category
      tasks.append(task)

  return tasks

def calculate_time_availability(all_events, tasks, end):
  for task in tasks:
    if not 'end' in task: task['end'] = "%d/%d" % (end.month, end.day)
  tasks = sorted(tasks, key = lambda x: x['end'])
  import ipdb; ipdb.set_trace()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None, help="yaml file to load task data from.")
    parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use current time.")
    parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. If nothing set, will use end of current day.")
    parser.add_argument("-t", "--timezone", default="US/Pacific")
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args()

    tzinfo = tz.gettz(args.timezone)

    task_data = load_yaml(args.file)

    service = setup_calendar()
    calendar_list = load_calendars_from_file()
    calendars = get_calendars_info(service, calendar_list)

    start, end = load_start_end(args.start, args.end, tzinfo)
    all_events = load_events(service, calendars, start, end)
    calculate_time_availability(all_events, flatten_tasks(task_data), end)
if __name__ == '__main__':
  main()