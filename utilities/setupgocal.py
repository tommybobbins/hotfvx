#!/usr/bin/python3
import caldav
import random
from datetime import datetime, date
import sys
url='http://localhost:80/'
username='hotf'
password='hotf'
client = caldav.DAVClient(url=url, username=username, password=password)
#client = caldav.DAVClient(url=url)
my_principal = client.principal()
## The principals calendars can be fetched like this:
print (my_principal)
calendars = my_principal.calendars()

## Let's try to find or create a calendar ...
try:
    ## This will raise a NotFoundError if calendar does not exist
    my_water_calendar = my_principal.calendar(name="water")
    assert(my_water_calendar)
    ## calendar did exist, probably it was made on an earlier run
    ## of this script
except caldav.error.NotFoundError:
    ## Let's create a calendar
    my_water_calendar = my_principal.make_calendar(name="water")

## Let's try to find or create a calendar ...
try:
    ## This will raise a NotFoundError if calendar does not exist
    my_heat_calendar = my_principal.calendar(name="heat")
    assert(my_heat_calendar)
    ## calendar did exist, probably it was made on an earlier run
    ## of this script
except caldav.error.NotFoundError:
    ## Let's create a calendar
    my_heat_calendar = my_principal.make_calendar(name="heat")

def create_ics(calendar,start,stop,summary):
    uid = start + str(random.randint(0,8192)) + summary
    assert(calendar)
    #print (uid)
    print(f"{start} {stop} {summary} {uid}")
    ical_string=str(f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTIMEZONE
TZID:Europe/London
BEGIN:DAYLIGHT
DTSTART:19810327T010000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
TZNAME:BST
TZOFFSETFROM:+0000
TZOFFSETTO:+0100
END:DAYLIGHT
X-LIC-LOCATION:Europe/London
END:VTIMEZONE
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{start}Z
DTSTART;TZID=Europe/London:{start}
DTEND;TZID=Europe/London:{stop}
RRULE:FREQ=WEEKLY
SUMMARY:{summary}
END:VEVENT
END:VCALENDAR
""")
#    print (ical_string)
    my_event = calendar.save_event(ical_string)

#Sat
create_ics(my_water_calendar,'20220205T000000','20220205T043000','water=false')
create_ics(my_water_calendar,'20220205T043001','20220205T110000','water=true')
create_ics(my_water_calendar,'20220205T110001','20220205T150000','water=false')
create_ics(my_water_calendar,'20220205T150001','20220205T200000','water=true')
create_ics(my_water_calendar,'20220205T200001','20220205T235959','water=false')

create_ics(my_heat_calendar,'20220205T000000','20220205T050000','temp=7')
create_ics(my_heat_calendar,'20220205T050001','20220205T110000','temp=20')
create_ics(my_heat_calendar,'20220205T110001','20220205T140000','temp=7')
create_ics(my_heat_calendar,'20220205T140001','20220205T230000','temp=20')
create_ics(my_heat_calendar,'20220205T230001','20220205T235959','temp=7')

#Sun
create_ics(my_water_calendar,'20220206T000000','20220206T053000','water=false')
create_ics(my_water_calendar,'20220206T053001','20220206T110000','water=true')
create_ics(my_water_calendar,'20220206T110001','20220206T150000','water=false')
create_ics(my_water_calendar,'20220206T150001','20220206T200000','water=true')
create_ics(my_water_calendar,'20220206T200001','20220206T235959','water=false')

create_ics(my_heat_calendar,'20220206T000000','20220206T050000','temp=7')
create_ics(my_heat_calendar,'20220206T050001','20220206T110000','temp=20')
create_ics(my_heat_calendar,'20220206T110001','20220206T140000','temp=7')
create_ics(my_heat_calendar,'20220206T140001','20220206T230000','temp=20')
create_ics(my_heat_calendar,'20220206T230001','20220206T235959','temp=7')

#Mon
create_ics(my_water_calendar,'20220207T000000','20220207T043000','water=false')
create_ics(my_water_calendar,'20220207T043001','20220207T080000','water=true')
create_ics(my_water_calendar,'20220207T080001','20220207T150000','water=false')
create_ics(my_water_calendar,'20220207T150001','20220207T200000','water=true')
create_ics(my_water_calendar,'20220207T200001','20220207T235959','water=false')

create_ics(my_heat_calendar,'20220207T000000','20220207T050000','temp=7')
create_ics(my_heat_calendar,'20220207T050001','20220207T080000','temp=20')
create_ics(my_heat_calendar,'20220207T080001','20220207T150000','temp=7')
create_ics(my_heat_calendar,'20220207T150001','20220207T230000','temp=20')
create_ics(my_heat_calendar,'20220207T230001','20220207T235959','temp=7')

#Tue
create_ics(my_water_calendar,'20220208T000000','20220208T043000','water=false')
create_ics(my_water_calendar,'20220208T043001','20220208T080000','water=true')
create_ics(my_water_calendar,'20220208T080001','20220208T150000','water=false')
create_ics(my_water_calendar,'20220208T150001','20220208T200000','water=true')
create_ics(my_water_calendar,'20220208T200001','20220208T235959','water=false')

create_ics(my_heat_calendar,'20220208T000000','20220208T050000','temp=7')
create_ics(my_heat_calendar,'20220208T050001','20220208T080000','temp=20')
create_ics(my_heat_calendar,'20220208T080001','20220208T150000','temp=7')
create_ics(my_heat_calendar,'20220208T150001','20220208T230000','temp=20')
create_ics(my_heat_calendar,'20220208T230001','20220208T235959','temp=7')

#Wed
create_ics(my_water_calendar,'20220209T000000','20220209T043000','water=false')
create_ics(my_water_calendar,'20220209T043001','20220209T080000','water=true')
create_ics(my_water_calendar,'20220209T080001','20220209T150000','water=false')
create_ics(my_water_calendar,'20220209T150001','20220209T200000','water=true')
create_ics(my_water_calendar,'20220209T200001','20220209T235959','water=false')

create_ics(my_heat_calendar,'20220209T000000','20220209T050000','temp=7')
create_ics(my_heat_calendar,'20220209T050001','20220209T080000','temp=20')
create_ics(my_heat_calendar,'20220209T080001','20220209T150000','temp=7')
create_ics(my_heat_calendar,'20220209T150001','20220209T230000','temp=20')
create_ics(my_heat_calendar,'20220209T230001','20220209T235959','temp=7')

#Thu
create_ics(my_water_calendar,'20220210T000000','20220210T043000Z','water=false')
create_ics(my_water_calendar,'20220210T043001','20220210T080000Z','water=true')
create_ics(my_water_calendar,'20220210T080001','20220210T150000Z','water=false')
create_ics(my_water_calendar,'20220210T150001','20220210T200000Z','water=true')
create_ics(my_water_calendar,'20220210T200001','20220210T235959Z','water=false')

create_ics(my_heat_calendar,'20220210T000000','20220210T050000','temp=7')
create_ics(my_heat_calendar,'20220210T050001','20220210T080000','temp=20')
create_ics(my_heat_calendar,'20220210T080001','20220210T150000','temp=7')
create_ics(my_heat_calendar,'20220210T150001','20220210T230000','temp=20')
create_ics(my_heat_calendar,'20220210T230001','20220210T235959','temp=7')

#Fri
create_ics(my_water_calendar,'20220211T000000','20220211T043000','water=false')
create_ics(my_water_calendar,'20220211T043001','20220211T080000','water=true')
create_ics(my_water_calendar,'20220211T080001','20220211T150000','water=false')
create_ics(my_water_calendar,'20220211T150001','20220211T200000','water=true')
create_ics(my_water_calendar,'20220211T200001','20220211T235959','water=false')

create_ics(my_heat_calendar,'20220211T000000','20220211T050000','temp=7')
create_ics(my_heat_calendar,'20220211T050001','20220211T080000','temp=20')
create_ics(my_heat_calendar,'20220211T080001','20220211T150000','temp=7')
create_ics(my_heat_calendar,'20220211T150001','20220211T230000','temp=20')
create_ics(my_heat_calendar,'20220211T230001','20220211T235959','temp=7')
exit()
