#!/usr/bin/python3
# Modified 30-Oct-2013
# tng@chegwin.org
# Retrieve: 
# 1: current temperature from radicale
# 2: Send to redis
# Modified 1-May-2022
# tng@chegwin.org
# Use environment variables from Docker
# 

import caldav
from datetime import datetime, date
import sys,time
from sys import path
from time import sleep
import re
import redis
import os
import caldav
from calculate_seconds import convert_time

Debug=(os.environ['HOTF_DEBUG'])
rediscalendar=(os.environ['HOTF_RADICALE_URL'])
redishost=(os.environ['HOTF_REDISHOST'])
redisport=int(os.environ['HOTF_REDISPORT'])
redisdb=int(os.environ['HOTF_REDISDB'])
redistimeout=int(os.environ['HOTF_REDISTIMEOUT'])
time_to_live=int(convert_time(os.environ['HOTF_REDISTTL']))
redthis=redis.StrictRedis(host=redishost,port=redisport, db=redisdb, socket_timeout=redistimeout)
radicale=(os.environ['HOTF_RADICALE_URL'])
radicale_user=(os.environ['HOTF_RADICALE_USER'])
radicale_pass=(os.environ['HOTF_RADICALE_PASS'])

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


try: 
    client = caldav.DAVClient(url=radicale, username=radicale_user, password=radicale_pass)
    my_principal = client.principal()
    ## The principals calendars can be fetched like this:
    calendars = my_principal.calendars()
    cal_water_bool=get_calendar('water').split("=")[-1]
    cal_heat_temp=float(get_calendar('heat').split("=")[-1])
    if Debug:
        print (f"Water={cal_water_bool}, Heat={cal_heat_temp}")
    redthis.set("calendar/water/requestedstate",cal_water_bool)
    redthis.set("calendar/heat/requestedstate",cal_heat_temp)
    redthis.expire("calendar/water/requestedstate",time_to_live)
    redthis.expire("calendar/heat/requestedstate",time_to_live)
except:
    print ("Unable to retrieve temperature")
