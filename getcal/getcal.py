#!/usr/bin/python3
import caldav
import sys
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument("-c", "--config", dest="filename",
                    help="Read config from filename", metavar="filename")
args = my_parser.parse_args()

from sys import path
import configparser
import datetime
from time import sleep
parserfile = configparser.ConfigParser()
parserfile.read(args.filename)

debug=parserfile.get('main','debug') # As string
Debug = {'True': True, 'False': False}.get(debug, False) # As Boolean
url=parserfile.get('calendar','url')
username=parserfile.get('calendar','username')
password=parserfile.get('calendar','password')
rotation_time=int(parser.get('main','rotation_time'))


def get_calendar(url, username, password, calendar):
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

while True:
  my_water=get_calendar(url,username,password,'water')
  my_heat=get_calendar(url,username,password,'heat')
  # write_to_water
  # write_to_heating
  sleep (rotation_time)

  if Debug:
      print (f"{my_water} \n{my_heat}")
