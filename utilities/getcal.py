#!/usr/bin/python3
import caldav
import sys
url='http://hotf/hotf/'
username='hotf'
password='hotf'
client = caldav.DAVClient(url=url, username=username, password=password)
my_principal = client.principal()
Debug=False
## The principals calendars can be fetched like this:
calendars = my_principal.calendars()

def get_calendar(calendar):
    from datetime import datetime, date
    if Debug:
        print (f"Getting data for {calendar}")
    try:
        my_local_calendar = my_principal.calendar(name=calendar)
        assert(my_local_calendar)
        events_fetched = my_local_calendar.date_search(
            start=datetime.now(), end=datetime.now(), expand=True)
    except:
        print("Your calendar server does apparently not support expanded search")
        events_fetched = my_local_calendar.date_search(
            start=datetime.now(), end=datetime.now(), expand=False)
    if Debug:
        print(events_fetched[0].data)
    return (events_fetched[0].vobject_instance.vevent.summary.value)


my_water=get_calendar('water')
my_heat=get_calendar('heat')

print (f"Water={my_water}, Heat={my_heat}")
