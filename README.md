* Follow [these steps](https://developers.google.com/calendar/quickstart/python) to 
  * turn on the Google Calendar API for this app and 
  * get credentials which will allow this app to interface with the Google Calendar API


## Todo
1. **Function: read.py**~~read in all the calendar events between a set start and end time~~
    a. option to save to yaml file
2. **Function: remove.py**. Clear all the calendar events between a set start and end time
3. **Function: put.py**. from a yaml file, set events by time for a given day
    a. can also be multi-day. some setting for this. when multi-day, `day:1`, `day:2`, etc. in yaml file.
4. **Function: move.py**. Pick calendar(s) and event time-frame and move events in time frame.
    a. move all events in time-frame up/down by x time (days or hours + minutes or both?)
    b. filter for things you don't want to be moved
    c. can also move all events starting at event named "x" on day y up. for multiple events of same day, can but `-n` option for which one. e.g from `-e block -n 2` would be block 2.


## Resources
1. [Google Calendar API](https://developers.google.com/calendar/)