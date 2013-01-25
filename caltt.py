#!/usr/bin/env python2.7
# coding=utf-8

from __future__ import division, print_function

import collections
import datetime
import dateutil.parser
import httplib2
import json
import pytz
import sys
import urllib

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

with open('settings.json') as settings_file:
    SETTINGS = json.load(settings_file)

storage = Storage('__credentials__')
credentials = storage.get()

if not credentials:
    flow = OAuth2WebServerFlow(
        client_id=SETTINGS['client_id'],
        client_secret=SETTINGS['client_secret'],
        scope="https://www.googleapis.com/auth/calendar.readonly",
        redirect_uri="urn:ietf:wg:oauth:2.0:oob"
    )
    auth_uri = flow.step1_get_authorize_url()
    print("Please open\n\n{}\n\nand insert the resulting code here.".format(auth_uri))
    code = raw_input("Code: ")
    credentials = flow.step2_exchange(code)
    storage.put(credentials)

http = httplib2.Http()
http = credentials.authorize(http)

start = datetime.datetime(2013, 1, 14, tzinfo=pytz.timezone("Europe/Berlin"))
end = start + datetime.timedelta(weeks=1)

REQUEST = "https://www.googleapis.com/calendar/v3/calendars/{}/events?timeMin={}&timeMax={}".format(
    urllib.quote(SETTINGS['cal_id']),
    urllib.quote(start.isoformat()),
    urllib.quote(end.isoformat())
)

response, content = http.request(REQUEST)
if response.status != 200:
    print(response)
    sys.exit(response.status)

events = json.loads(content)['items']

Event = collections.namedtuple('Event', ['title', 'type', 'location', 'start', 'end'])
TIMETABLE = collections.defaultdict(list)
for event in map(
    lambda _e: Event(
        _e['summary'],
        _e['summary'].split(" ")[-1],
        _e['location'],
        dateutil.parser.parse(_e['start']['dateTime']),
        dateutil.parser.parse(_e['end']['dateTime'])
    ),
    events
):
    TIMETABLE[event.start.weekday()].append(event)

for day in TIMETABLE:
    print(DAYS[day])
    for _e in TIMETABLE[day]:
        print(u"{1} {0}".format(_e.title, _e.start.strftime("%H:%M")))
