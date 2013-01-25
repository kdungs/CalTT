#!/usr/bin/env python2.7
# coding=utf-8

import datetime
import dateutil.parser
import httplib2
import json
import pytz
import sys
import urllib

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

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

_start = datetime.datetime(2013, 1, 14, tzinfo=pytz.timezone("Europe/Berlin"))
_end = _start + datetime.timedelta(weeks=1)

REQUEST = "https://www.googleapis.com/calendar/v3/calendars/{}/events?timeMin={}&timeMax={}".format(
    urllib.quote(SETTINGS['cal_id']),
    urllib.quote(_start.isoformat()),
    urllib.quote(_end.isoformat())
)

response, content = http.request(REQUEST)
if response.status != 200:
    print(response)
    sys.exit(response.status)

calendar = json.loads(content)
events = calendar['items']

TIMETABLE = {}

for event in events:
    if event.has_key('recurrence'):
        start = dateutil.parser.parse(event['start']['dateTime'])
        end = dateutil.parser.parse(event['end']['dateTime'])
        TIMETABLE[start] = {
            'title': event['summary'],
            'type': event['summary'].split(" ")[-1],
            'location': event['location'],
            'start': start,
            'end': end
        }
        if event.has_key('description'):
            TIMETABLE[start]['description'] = event['description']

TT_by_day = [[
    TIMETABLE[x] for x in TIMETABLE.iterkeys() if TIMETABLE[x]["start"].weekday() == day
] for day in range(5)]

for day in range(5):
    print(DAYS[day])
    for event in sorted(TT_by_day[day], key=lambda t: t['start'].time()):
        print(u"{1} {0}".format(event['title'], event['start'].strftime("%H:%M")))
