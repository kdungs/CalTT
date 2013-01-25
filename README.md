# CalTT
Generate a nice timetable from your Google Calendar.

## Warning
**This code is heavily under development.** Don't expect anything to work yet.

## What's this?
Google Calendar is a pretty nifty thing you might use every day. However when it comes to planning your weekly schedule in school or university you might want something more timetable-ish. This is where CalTT - short for **Cal**endar **T**ime **T**able - comes into play. Since you probably have already put all your relevant events (lectures, tutorials, etc.) in a seperate calendar (e.g. labeled "University"), using CalTT is easily done in four steps:
 * Obtain your calendar's ID (looks something like randommixoflettersanddigits@group.calendar.google.com)
 * Clone this repository
 * _[Generate an OAuth Key](https://code.google.com/apis/console) (For your own safety at this point… Likely to be improved/removed in future versions.)_
 * Run `caltt.py` _(At this point there is no HTML output, yet. This is soon to be added, of course.)_

## Settings
You have to have a `settings.json` file present in the same directory as caltt.py. It should look like the following:
```json
{
    "cal_id": "<YOUR CALENDAR ID>",
    "client_id": "<YOUR APP'S CLIENT ID>",
    "client_secret": "<YOUR APP'S CLIENT SECRET>"
}
```
where you have to replace the values in brackets, of course.

## License
All of the code in this project, if not stated otherwise, is licensed under the terms of the MIT License.

    The MIT License (MIT)
    Copyright (c) 2012 Kevin D. (https://github.com/SirCoemgen)

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
