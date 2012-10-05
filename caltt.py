#!/usr/bin/env python
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

storage = Storage('__credentials__')
credentials = storage.get()

if not credentials:
    flow = OAuth2WebServerFlow(
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>",
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

CAL_ID = "<YOUR CALENDER ID>"
_start = datetime.datetime(2012, 10, 8, tzinfo=pytz.timezone("Europe/Berlin"))
_end = _start + datetime.timedelta(weeks=1)

REQUEST = "https://www.googleapis.com/calendar/v3/calendars/{}/events?timeMin={}&timeMax={}".format(
    urllib.quote(CAL_ID),
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
            'description': event['description'],
            'start': start,
            'end': end
        }

for key in sorted(TIMETABLE):
    print(key)
    for k, v in TIMETABLE[key].iteritems():
        print(u"{}:\t{}".format(k, v))
    print("")



"""
# for later
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

# …

QTapp = QApplication(sys.argv)

QTweb = QWebView()
QTweb.load(QUrl(auth_uri))
QTweb.show()

sys.exit(QTapp.exec_())
"""
