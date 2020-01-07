"""
    available_time.py by Wilka Carvalho
"""
# python utils
import argparse
from termcolor import colored
# import hashlib


# date utilities
from dateutil.parser import parse
from dateutil import tz

# this library
from calendar_automator.lib import get_calendars_info, setup_calendar, load_start_end, load_calendars_from_file
from calendar_automator.read import load_events


colors = ["red", "green", "yellow", "magenta", "cyan"]
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def half_round(x):
  # round to nearest quester
  return round(x*2)/2

def quarter_round(x):
  # round to nearest quester
  return round(x*4)/4

def tenth_round(x):
  # round to nearest quester
  return round(x*10)/10

def calculate_daily_available(events, raw_end, end, tzinfo, to_skip='_block'):

  indx = -1
  days = set()
  times = {}
  for event in events:
    summary = event['summary']
    if summary != "block": continue

    event_start = event['start']['dateTime'].replace(tzinfo=tzinfo)
    event_end = parse(event['end']['dateTime']).replace(tzinfo=tzinfo)
    dif = event_end - event_start
    minutes = dif.total_seconds()/60
    hours = minutes/60

    # import ipdb; ipdb.set_trace()
    start_day = event_start.day
    start_month = event_start.month
    start_day_indx = event_start.weekday()
    day = "%s %d/%d" % (day_names[start_day_indx], start_month, start_day)

    if day in days:
      key = "%d. %s" % (indx, day)
      times[day] += hours
    else:
      indx += 1
      days.add(day)
      key = "%d. %s" % (indx, day)
      times[day] = hours

  if not times: return
  print("\n\n------Daily Available Time------")

  max_len = 6

  max_key_len = max([len(i) for i in times.keys()])
  for key in times:
    apx_time = half_round(times[key])
    apx_percent = tenth_round(apx_time/max_len)

    start = ("%s: %.2f" % (key.ljust(max_key_len+1), apx_time))
    print("%s = %s" % (start, "x"*int(8*apx_time)))



def calculate_time_scheduled(events, raw_end, end, tzinfo):

  nevents = len(events)

  def split_category_activity(string):
    split = string.split(":")
    # print(split)
    # if len(split) > 2:
    #   import ipdb; ipdb.set_trace()
    if len(split) == 1:
      return split[0].strip(), split[0].strip()
    elif len(split) == 2:
      return split[0].strip(), split[1].strip()
    elif len(split) == 0:
      raise RuntimeError("empty string?")
    else:
      # import ipdb; ipdb.set_trace()
      return split[0], ":".join(split[1:]).strip()

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
  # try: print("Total Unscheduled: %2.2f" % (tasks['block']['block']/60))
  # except: pass

  for color_indx, category in enumerate(sorted(tasks.keys())):
    # if category == 'block': continue
    total_per_category = 0
    for indx, activity in enumerate(tasks[category]):
      minutes = tasks[category][activity]
      total_per_category += minutes

    color_indx = (color_indx - 1)%len(colors)

    if len(tasks[category]) == 1:
      key = [i for i in tasks[category].keys()][0]
      print()
      if category == key:
        print("%s: %2.2f" % (colored(key, colors[color_indx]), total_per_category/60))
      else:
        print("%s: %s: %2.2f" % (colored(category, colors[color_indx]), key, total_per_category/60))
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
    parser.add_argument("-t", "--timezone", default="US/Eastern")
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

    # turn start dateTime into a datetime object for all events
    for event in combined_events:
      event['start']['dateTime'] = parse(event['start']['dateTime'])
    combined_events = sorted(combined_events, key = lambda x: x['start']['dateTime'])

    calculate_time_scheduled(combined_events, args.end, end, tzinfo)

    calculate_daily_available(combined_events, args.end, end, tzinfo)


if __name__ == '__main__':
  main()