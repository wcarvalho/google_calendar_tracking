"""Summary

Attributes:
    term (TYPE): Description
"""

# get path of file
import sys
import os
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
from calendar_automator.lib import get_calendar_dicts, load_calendar_service, load_start_end
from calendar_automator.read import load_events



term = Terminal()
def customround(x, base=5):
    return base * round(x/base)

def split_project_task(task):
  """Assume format:
    project: task
    returns project, task
  """
  task = task.replace("\n", ". ")
  split = task.split(":", 1)

  if len(split) == 1:

    return split[0].strip(), ""
  elif len(split) == 2:
    # project, task
    return split[0].strip(), split[1].strip()
  elif len(split) == 0:
    raise RuntimeError("empty string?")
  else:
    return split[0], ":".join(split[1:]).strip()

def compute_event_length(event, tzinfo):
  """Compute the number of hours for the duration of an event"""
  event_start = event['start']['dateTime'].replace(tzinfo=tzinfo)
  event_end = parse(event['end']['dateTime']).replace(tzinfo=tzinfo)
  dif = event_end - event_start
  minutes = dif.total_seconds()/60/60
  return minutes

def format_task(task):
  # beginning = task.find("[")
  # end = task.find("]")+1
  # if beginning > -1:
  #   sub = task[beginning: end]
  #   task = task.replace(sub, "")
  return task


def multitask_project_lines(project, time, time_percent, total_time, fulltask2length, fulltask2task, fulltask_names, line_divider):
  """
    Get multi-line project lines. e.g., in format
    Project                              x          x
              1. task 1                  x          x
              2. task 2                  x          x
  """
  lines = []
  line = [project.capitalize(), '(total)', "%.1f" % time, "%2.f" % time_percent]
  lines.append(line_divider)
  lines.append(line)

  for indx, fulltask_name in enumerate(fulltask_names):
    task = format_task(fulltask2task[fulltask_name])
    if not task: continue
    time = fulltask2length[fulltask_name]
    time_percent = 100*(time/total_time)


    line = ['', f"{indx+1}. {task}",  "%.1f" % time, "%2.f" % time_percent]
    # print(line)
    # import ipdb; ipdb.set_trace()
    lines.append(line)
  return lines

def singletask_project_line(project, time, time_percent, fulltask2length, fulltask2task, fulltask_names, line_divider):
  # -----------------------
  # get task information
  # -----------------------
  fulltask_name = fulltask_names[0]
  indx = 1
  task = format_task(fulltask2task[fulltask_name])

  lines = [line_divider]
  line = [project.capitalize(), task, "%.1f" % time, "%2.f" % time_percent]
  lines.append(line)

  return lines


# ======================================================
# main functions
# ======================================================
def calculate_time_per_task(events, raw_end, end, tzinfo, 
  assignable=[],
  ):
  assignable = set(assignable)
  nevents = len(events)

  # stores total time for project
  project2length = collections.defaultdict(float)

  # stores total time for individual tasks
  fulltask2length = collections.defaultdict(float)

  # stores taskname --> project
  fulltask2project=collections.defaultdict(str)

  # stores taskname --> task
  fulltask2task=collections.defaultdict(str)

  # ======================================================
  # get time for all tasks
  # ======================================================
  for event in events:
    fulltask_name = event['summary'].lower()
    project, task = split_project_task(fulltask_name)
    if project in assignable:
      fulltask_name = project = "unscheduled"

    fulltask2project[fulltask_name] = project
    fulltask2task[fulltask_name] = task

    length = compute_event_length(event, tzinfo)
    fulltask2length[fulltask_name] += length

  # ======================================================
  # get time assigned at project-level
  # ======================================================
  project2fulltasks = collections.defaultdict(list)
  for fulltask_name, length in fulltask2length.items():
    project = fulltask2project[fulltask_name]
    project2length[project] += length
    project2fulltasks[project].append(fulltask_name)

  total_time = sum(project2length.values())


  # ======================================================
  # Want to print in a hierarchical manner:
  # Project| Task | Time | % Total Time
  # ======================================================
  header=["Project","Task", "Time: %.1f" % total_time, "Percent"]
  lines = [header]
  title_lengths = [len(x) for x in header]


  # -----------------------
  # create line_divider between projects
  # -----------------------
  max_project_length = len(max(project2fulltasks.keys(), key=lambda x: len(x)))
  formatted_tasknames = [format_task(t) for t in fulltask2task.values()]
  max_task_length = len(max(formatted_tasknames, key=lambda x: len(x)))
  line_divider = ["-"*(max_project_length+1),
                  "-"*(max_task_length+3),
                  "-"*(title_lengths[2]+1),
                  "-"*(title_lengths[3]+1)]


  # -----------------------
  # create table
  # -----------------------
  # first remove dummy `unscheduled` and add it manually
  project = 'unscheduled'
  time = project2length[project]
  time_percent = 100*(time/total_time)
  project2fulltasks.pop(project, None)
  lines.extend(singletask_project_line(project, time, time_percent, fulltask2length, fulltask2task, [project], line_divider))



  # then add the rest
  for project, fulltask_names in project2fulltasks.items():
    time = project2length[project]
    time_percent = 100*(time/total_time)

    if len(fulltask_names) > 1:
      new_lines = multitask_project_lines(
        project=project,
        time=time,
        time_percent=time_percent,
        total_time=total_time,
        fulltask2length=fulltask2length,
        fulltask2task=fulltask2task,
        fulltask_names=fulltask_names,
        line_divider=line_divider
        )

    elif len(fulltask_names) == 1:
      new_lines = singletask_project_line(project, time, time_percent, fulltask2length, fulltask2task, fulltask_names, line_divider)
    else:
      raise NotImplementedError
    lines.extend(new_lines)


  print(tabulate(lines, tablefmt="pretty"))


def calculate_time_per_day(events,
    raw_end,
    end,
    tzinfo,
    assignable=['block', 'deep-work', 'paper'],
    round_base=.25,
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    """
    Print out the amount of time available for each day
    """

    indx = -1
    days = set()
    assignable = set(assignable)

    time_per_day = collections.defaultdict(float)

    for event in events:
        eventname = event['summary'].strip()
        if not (eventname in assignable): continue


        # -----------------------
        # get the day information
        # -----------------------
        event_start = event['start']['dateTime'].replace(tzinfo=tzinfo)
        start_day = event_start.day
        start_month = event_start.month
        start_day_indx = event_start.weekday()
        day = "%s %d/%d" % (day_names[start_day_indx], start_month, start_day)

        hours = compute_event_length(event, tzinfo)
        time_per_day[day] += hours


    if not time_per_day: return

    total_time = sum(time_per_day.values())
    # -----------------------
    # now print
    # -----------------------
    header = ["Day","Time: %.1f" % customround(total_time, round_base), "Percent", '']
    lines = []
    for day, time in time_per_day.items():
        rounded_time = customround(time, round_base)

        time_percent = 100*(time/total_time)
        blocks = "x"*int((1/round_base)*rounded_time)
        line = [day, "%.1f" % rounded_time, "%2.f" % time_percent, blocks]
        lines.append(line)


    print(tabulate(lines, headers=header, tablefmt="pretty"))


# ======================================================
# program
# ======================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", default=None, help="start time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. default: current time.")
    parser.add_argument("-e", "--end", default=None, help="end time. format: month/day/year hour:minute, e.g. 5/20/2018 5:34. default: end of current day.")
    parser.add_argument("-t", "--timezone", default="US/Eastern", help="default: US/Eastern")
    args = parser.parse_args()

    tzinfo = tz.gettz(args.timezone)

    # ======================================================
    # load settings
    # ======================================================
    with open(SETTINGS_FILEPATH, 'r') as f:
        settings = yaml.load(f)

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

    calendars = get_calendar_dicts(calendar_service, 
        calendar_names=settings['calendars'])

    # ======================================================
    # get all events within that time-frame
    # ======================================================
    calendar2event = load_events(calendar_service, calendars, start, end, tzinfo) # per calendar
    all_events = [] # combined across calendars
    for calendar in calendars:
      all_events += calendar2event[calendar]


    # turn start dateTime into a datetime object for all events
    for event in all_events:
      event['start']['dateTime'] = parse(event['start']['dateTime'])
    # sort by starting time
    all_events = sorted(all_events, key = lambda x: x['start']['dateTime'])


    print(term.orangered("="*15 + " Task Time Distribtuon " + "="*15))
    calculate_time_per_task(all_events, args.end, end, tzinfo,
      assignable=settings['assignable']
      )


    print("\n")
    print(term.darkgoldenrod1("="*15 + " Unscheduled Daily Time Distribtuon " + "="*15))
    calculate_time_per_day(all_events, args.end, end, tzinfo,
        assignable=settings['assignable'],
        )



if __name__ == '__main__':
  main()