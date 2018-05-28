import yaml
import argparse
import pprint

from lib import load_yaml

def required_time(data, tasks):
  time_needed = 0
  for task in tasks:
    task_data = data[task]
    for entry in task_data:
      if not 'time' in entry:
        continue 
      task_time = entry['time']
      if 'repeat' in entry: task_time *= int(entry['repeat'])
      time_needed += task_time
  return time_needed

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", default=None, help="yaml file to load data from.")
  args = parser.parse_args()

  data = load_yaml(args.file)
  
  tasks = list(data.keys())
  time_needed = required_time(data, tasks)
  print("Time needed for tasks is %d hours" %time_needed )


if __name__ == '__main__':
  main()