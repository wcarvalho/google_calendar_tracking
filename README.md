## Goal
I've wanted to template my calendars for years. I think each week is different, but I think weeks repeat. I like to schedule most of my time (even if I don't follow the schedule so strictly) so that I have a foundation to work from. These scripts are my attempt at doing so. The idea right now is to implement 4 functions
* read: this will read calendar events between in a time-frame (and optionally save them) 
* remove: this will remove calendar events in a time-frame
* put: this will put events into the calendar from a file
* move: this will move events within a time-frame "up" or "down"

Together, I should be able to create, save, load, and move events with these scripts. And I think this will facilitate maintaining and editing templates.

## Getting Started
* Follow [these steps](https://developers.google.com/calendar/quickstart/python) to 
  * turn on the Google Calendar API for this app and 
  * get credentials which will allow this app to interface with the Google Calendar API


## Todo
1. **Function: read.py**.
   * ~~read in all the calendar events between a set start and end time~~
   * ~~option to save to yaml file~~

2. **Function: remove.py**. 
   * Clear all the calendar events between a set start and end time

3. **Function: put.py**. 
   * Using a yaml file, set events for 
a given day
   * can also be multi-day. some setting for this. when multi-day, `day:1`, `day:2`, etc. in yaml file.

4. **Function: move.py**. 
   * Pick calendar(s) and event time-frame and move all events in time-frame up/down by x time (days or hours + minutes or both?)
   * filter for things you don't want to be moved
   * can also move all events starting at event named "x" on day y up. for multiple events of same day, can but `-n` option for which one. e.g from `-e block -n 2` would be block 2.


## Resources
1. [Google Calendar API](https://developers.google.com/calendar/)