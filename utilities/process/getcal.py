#!/usr/bin/python3
import caldav
import sys
import argparse

import datetime
from time import sleep

def get_calendar(url, username, password, calendar, Debug):
    client = caldav.DAVClient(url=url, username=username, password=password)
    my_principal = client.principal()

    ## The principals calendars can be fetched like this:
    calendars = my_principal.calendars()
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
        print(events_fetched[0].vobject_instance.vevent.summary.value)
    output_format = (events_fetched[0].vobject_instance.vevent.summary.value).split('=')
    return (events_fetched[0].vobject_instance.vevent.summary.value)

#my_water=get_calendar('http://radicale.radicale/','hotf','hotf','water')
#my_heat=get_calendar('http://radicale.radicale/','hotf','hotf','heat')

#if Debug:
#    print (f"{my_water} \n{my_heat}")
