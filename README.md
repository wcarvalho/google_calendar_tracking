## Getting Started

Step 1: Install.

```bash
pip install -e .
```


Step 2: setup google api: Follow [these steps](https://developers.google.com/calendar/quickstart/python) to
* turn on the Google Calendar API for this app and 
* get credentials (`credentials.json`, `client_secret.json`) which will allow this app to interface with the Google Calendar API 



Step 3: setup settings yamlfile. Create a file called `settings.yaml` and place it in this directory. It should contain the following:

  ```yaml
credentials: credentials.json # probably unchanged 
secret: client_secret.json # probably unchanged 

# calendars you want to load
calendars:
- "calendar 1"
- "calendar 2"

# name of events that will be used for assigning time
assignable:
- block
- deep-work
  ```

* `calendars`: The calendars within your gmail account you want to load data from
* `assignable`: The name used for events which you will treat as ''unassigned time". See example below.

## Example Usage

I assume calendar events follow the format: `project:task`.

```bash
time_dist --start 3/15 --end 3/17
```

Here's an example below with dummy data:
<table>
  <tr>
    <td>
      <img class="" src="misc/terminal.png">
    </td>
    <td>
      <img class="" src="misc/calendar.png">
    </td>
  </tr>
  <tr>
    <td>Example terminal call</td>
    <td>Corresponding calendar</td>
  </tr>
</table>



## Resources
1. [Google Calendar API](https://developers.google.com/calendar/)
2. [My time-management guide](https://wcarvalho.github.io/tutorial/2016/01/08/TimeManagementPrescription/)
