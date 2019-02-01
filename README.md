## Goal
I've wanted to template my calendars for years. I think each week is different, but I think weeks repeat. I like to schedule most of my time (even if I don't follow the schedule so strictly) so that I have a foundation to work from. These scripts are my attempt at doing so. The idea right now is to implement 4 functions
* read: this will read calendar events between in a time-frame (and optionally save them) 
* clear: this will clear calendar events in a time-frame
* put: this will put events into the calendar from a file
* move: this will move events within a time-frame "up" or "down"

Together, I should be able to create, save, load, and move events with these scripts. And I think this will facilitate maintaining and editing templates.



## Getting Started
* Follow [these steps](https://developers.google.com/calendar/quickstart/python) to 
  * turn on the Google Calendar API for this app and 
  * get credentials which will allow this app to interface with the Google Calendar API

* Create a file called `calendars.yaml` and place in it the calendars you which to track on Google Calendar. They should a `planning` key. (This was an arbitrary design choice that I forgot the motivation for) Mine looks like:

  ```yaml
  planning:
    - "1. urgent"
    - "4. papers"
    - "errands"
    - "appointments"
  ```

## Example Usage
```bash
# see time scheduled between 1/25 and 1/30
python scheduled_time.py -s 1/25 -e 1/30
```

**note**: If you name your calendar events `category:task`, the script will interpret show the tasks under a category as follows

![categories](figs/category_example.png)

## Workflow

You want create and experiment with multiple calendar templates to see which is best. For each one:
  1. Create a template for a week (or some time-length)
  1. Clear across dates that you want to apply this template (from appropriate calendars)
  1. Place from template across those dates
  1. run time-availability script to see buffer

## Todo


1: hierarchical indenting. functionality  (maybe)
2: times per day (more useful)

### Main Functions
1. **read.py**
   * ~~read in all the calendar events between a set start and end time~~
   * ~~option to save to yaml file~~

2. **clear.py** 
   * ~~Clear all the calendar events between a set start and end time~~
   * remove a single event or set of events in a time-range by the event name(s)

3. **put.py** 
   * ~~Using a yaml file, set events for a given day~~
      * ~~set events for multiple days (e.g. 2 days of worth of events)~~
      * ~~repeat both `>=1` (e.g. 1 or 2) days worth of events every `d` days `n` times~~

4. **move.py** 
   * Pick calendar(s) and event time-frame and move all events in time-frame up/down by x time (days or hours + minutes or both?)
   * filter for things you don't want to be moved
   * can also move all events starting at event named "x" on day y up. for multiple events of same day, can but `-n` option for which one. e.g from `-e block -n 2` would be block 2.

5. **replicate.py**
   * ~~replace the contents within a date-range with that from another date-range (potentially tiled)~~
   * option to replace from file

6. **required_time.py**
   * ~~calculates how much time you need for tasks in a task list defined by a yaml file~~

7. **available_time.py**
   * ~~Calculate some information on whether you have enough time for your tasks, and by how much if so (i.e. your buffer).~~
   * support for multiple calendars per task (currently a task can only be checked on one calendar)


### Other
1. A system of templates, their descriptions/notes with potential to add photos. This auto-populate PDF (or something).
1. Default settings yaml file (for things like timezone)
1. common command-line args across files.
   a. can input calendars from command line (currently just settings file)
<!-- 1. Function that clears previous authorization and redoes authorization -->

## Resources
1. [Google Calendar API](https://developers.google.com/calendar/)