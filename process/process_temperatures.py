# Modified 30-Oct-2013
# tng@chegwin.org
# Retrieve: 
# 1: target temperature from a calendar
# 2: current temperature from a TMP102 sensor
# 3: weather from the weather_file (or run weather_script and try again)
#    file is populated by weather-util. See retrieve-weather.sh for details
# Modified 24-June-2015
# tng@chegwin.org
# Move to django_happenings
# Modified 27-Sep-2015
# tng@chegwin.org/jon@rosslug.org.uk
# Modularised, added config file, made generic

filename="/data/pithermostat.conf"
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-c", "--config", dest="filename",
                    help="Read config from filename", metavar="filename")
args = parser.parse_args()


import localredis
from sys import path
from localredis import read_redis,write_redis,ttl_redis
import configparser
import datetime
from time import sleep
import redis
from relay_state import get_relay, send_relay
from calculate_temps import calculate_temps,calculate_weighted_mean
from getcal import get_calendar
import re
parser = configparser.ConfigParser()
parser.read(filename)

debug=parser.get('main','debug') # As string
Debug = {'True': True, 'False': False}.get(debug, False) # As Boolean
print ("Debug = %s\n" % Debug)
redishost=parser.get('redis','broker')
redisport=int(parser.get('redis','port'))
redisdb=parser.get('redis','db')
redistimeout=float(parser.get('redis','timeout'))
boiler_relay=parser.get('relays','boiler')
water_relay=parser.get('relays','water')
rotation_time=int(parser.get('main','rotation_time'))

print(f'{redishost} {redisport} {redisdb} {redistimeout}')

hysteresis_temp=float(parser.get('main','hysteresis_temp'))
summer_temp=float(parser.get('weather','summer_temp'))
summer_offset=float(parser.get('weather','summer_offset'))
#print ("Summer temp = %f" % summer_temp)
temp={}
multiplier={}
external_temp={}
external_multiplier={}

calendar_url=parser.get('calendar','url')
calendar_user=parser.get('calendar','username')
calendar_pass=parser.get('calendar','password')

heat_value=get_calendar(calendar_url,calendar_user,calendar_pass,'heat',Debug)
water_value=get_calendar(calendar_url,calendar_user,calendar_pass,'water',Debug)
print (f'heat_value={heat_value}, water_value = {water_value}')

def update_relayinfo():
   try:
       boiler_state=str(get_relay("boiler"))
       water_state=str(get_relay("water"))
   except:
       print ("Unable to get relay state")
   try:
       write_value=write_redis(redishost,redisport,redisdb,redistimeout,'relay/boiler',boiler_state,rotation_time)
       write_value=write_redis(redishost,redisport,redisdb,redistimeout,'relay/water',water_state,rotation_time)
   except:
       print ("Unable to set redis relay state")

def send_call_boiler(on_or_off):
    if Debug:
        print ("on/off = %s " % on_or_off)
    if (on_or_off == "on"):
        try:
            write_value=write_redis(redishost,redisport,redisdb,redistimeout,'boiler/req',"on",rotation_time)
            #redthis.set("boiler/req", "on")
            #redthis.expire("boiler/req", rotation_time)
            write_value=write_redis(redishost,redisport,redisdb,redistimeout,'boiler/4hourtimeout',"on",14400)
            #redthis.set("boiler/4hourtimeout", "on")
            #redthis.expire("boiler/4hourtimeout", 14400)
            #redthis.rpush("cellar/jobqueue", "/usr/local/bin/drayton on")
            send_relay("boiler","on")
        except:
            print ("Unable to update redis")
    elif (on_or_off == "off"):
        try:
            write_value=write_redis(redishost,redisport,redisdb,redistimeout,'boiler/req',"off",rotation_time)
            #redthis.set("boiler/req", "off")
            #redthis.expire("boiler/req", rotation_time)
            #redthis.rpush("cellar/jobqueue", "/usr/local/bin/drayton off")
            send_relay("boiler","off")
        except:
            print ("Unable to update redis")
    else:
        print ("Need to send on or off to send_call_boiler()")

def send_call_water():
    water_req="Lost"
    water_state="Lost"
    expiry_time=rotation_time/10
    try:
      expiry_time=ttl_redis(redishost,redisport,redisdb,redistimeout,'water/req')
      if read_redis(redishost,redisport,redisdb,redistimeout,'water/req'):
         water_req=read_redis(redishost,redisport,redisdb,redistimeout,'water/req')
      else:
         water_req=read_redis(redishost,redisport,redisdb,redistimeout,'water/req')
      water_cal=get_calendar(calendar_url,calendar_user,calendar_pass,'water',Debug).split("=")[-1]
      if Debug:
          print (f"water_cal array = {water_cal} {water_cal[1]}")
      write_value=write_redis(redishost,redisport,redisdb,redistimeout,'water/calendar',water_cal[1],0)
    except:
      write_value=write_redis(redishost,redisport,redisdb,redistimeout,'water/calendar',water_state,0)
      if Debug:
         print ("Expiry time of %s is %i . Calendar is %s" % (water_req,expiry_time,water_cal))
         print ("Lost one of %i, %s %s" % (expiry_time, water_req, water_cal))
    if ( expiry_time <= 60 ):
         # Water has not been manually boosted and we set to calendar
       try:
          if Debug:
              print ("Water temp = %s" % water_state)
          write_value=write_redis(redishost,redisport,redisdb,redistimeout,'water/req',water_cal,rotation_time)
          send_relay("water",water_cal)
       except: 
          water_state="Lost"
          if Debug:
             print ("Expiry time of %s is %i . Calendar is %s" % (water_req,expiry_time,water_state))
             print ("Something went wrong")
          #redthis.set("water/req", water_cal)
          write_value=write_redis(redishost,redisport,redisdb,redistimeout,'water/req',water_cal,rotation_time)
          #redthis.expire("water/req", rotation_time)
    elif ( expiry_time <= rotation_time ):
       if Debug:
          print ("Water state = %s %i" % (water_cal,expiry_time))
    else:
       # We are boosted
       if Debug:
          print ("Nothing to do, water is boosted = %s %i" % (water_req,expiry_time))
       send_relay("water",water_req)

def read_temps():
    try:
        heat_value_raw=get_calendar(calendar_url,calendar_user,calendar_pass,'heat',Debug)
        if Debug:
            print(f'heat_value={heat_value_raw}')
        heat_value=float(get_calendar(calendar_url,calendar_user,calendar_pass,'heat',Debug).split("=")[-1])
        if Debug:
            print(f'heat_split_value={heat_value}')
        calendar_temp=float(get_calendar(calendar_url,calendar_user,calendar_pass,'heat',Debug).split("=")[-1])
    except:
        print ("Google down or Django schedule not happening")
        calendar_temp=6.999
    try:
        #Read in all the previous settings
        weather_temp=float(read_redis(redishost,redisport,redisdb,redistimeout,'temperature/weather'))
        userreq_temp=float(read_redis(redishost,redisport,redisdb,redistimeout,'temperature/userrequested'))
        ##### Optimal temp is the debug value we want to set the house to
        ##### if all else fails
        failover_temp=float(read_redis(redishost,redisport,redisdb,redistimeout,'temperature/failover'))
    except:
        print ("Unable to find redis stats")
        weather_temp=14.999
        userreq_temp=6.999
        time_to_live=290
        failover_temp = 14.663
        previous_calendar_temp=calendar_temp

    try:
        (mean_temp, mean_external_temp) = calculate_temps()
    except:
        mean_temp=15.623
        mean_external_temp=10.123
    try:
        outside_rolling_mean=float(read_redis(redishost,redisport,redisdb,redistimeout,'temperature/outside/rollingmean'))
    except:
        outside_rolling_mean = 6.33
    # Store our previous google calendar temperature for ref.
    previous_calendar_temp=read_redis(redishost,redisport,redisdb,redistimeout,'heat/calendar')
    boiler_state=(read_redis(redishost,redisport,redisdb,redistimeout,'boiler/req'))
#    time_to_live=int(redthis.ttl("boiler/req"))
    time_to_live=int(ttl_redis(redishost,redisport,redisdb,redistimeout,'boiler/req'))
    # Store our google calendar temperature for future reference
    if (outside_rolling_mean >= summer_temp):
        calendar_temp += -summer_offset
        if Debug:
            print ("Calendar temp = %f" % calendar_temp)
            print ("Outside Rolling mean temp = %f" % outside_rolling_mean)
            print ("Summer temp = %f" % summer_temp)
#    else:
#        print ("It is not summer")
    write_value=write_redis(redishost,redisport,redisdb,redistimeout,'heat/calendar',calendar_temp,0)

    if Debug: 
        print ("Found weather %f" % weather_temp)
        print ("Found user requested %f" % userreq_temp)
        print ("Found calendar %f" % calendar_temp)
        print ("Time until boiler needs poking = %i" % time_to_live)
        print (f"Previous calendar {previous_calendar_temp}")
        print ("Calendar_temp = %f" % calendar_temp)
    if (previous_calendar_temp != calendar_temp):
        #Calendar appointment has changed. Reset User Requested temperature 
        userreq_temp=calendar_temp 
        if Debug:
            print (f"Previous {previous_calendar_temp}, current_calendar {calendar_temp}")
            print (f"User Requested {userreq_temp} is not equal to calendar {calendar_temp}")
        try:
            #redthis.set("temperature/userrequested", userreq_temp)
            write_value=write_redis(redishost,redisport,redisdb,redistimeout,'temperature/userrequested',userreq_temp,0)
        except:
            print ("Unable to update redis")
    if Debug:
        print ("User Requested is now %f" % userreq_temp)
    #redthis.set("temperature/inside/weightedmean", mean_temp)
    write_value=write_redis(redishost,redisport,redisdb,redistimeout,'temperature/inside/weightedmean',mean_temp,0)
    #redthis.set("temperature/outside/weightedmean", mean_external_temp)
    write_value=write_redis(redishost,redisport,redisdb,redistimeout,'temperature/outside/weightedmean',mean_external_temp,0)
    if Debug:
        print ("Mean temperature = %f" % mean_temp)

#   If in holiday mode, then keep userreq_temp at holiday_countdown
    try:
        #userreq_temp = float(redthis.get("holiday_countdown"))
        userreq_temp=float(read_redis(redishost,redisport,redisdb,redistimeout,'holiday_countdown'))

        if Debug:
            print ("Holiday mode: User Requested Temp = %f" % userreq_temp)
    except:
        if Debug:
            print ("Not in holiday Mode")

    if (time_to_live <= (int(rotation_time / 9))): 
        if Debug:
            print ("Time to live is <= 35 seconds")
            print ("Time to live is %i" % (int(rotation_time/9)))
        working_temp = userreq_temp + hysteresis_temp
        # e.g. 21.3 = 20.0 + 1.3
        if (mean_temp <= userreq_temp):
#            e.g. Temp is 16.0
            send_call_boiler("on")
            if Debug:
                print ("Switching on")
        elif (mean_temp >= working_temp):
#            e.g. Temp is 21.3
            send_call_boiler("off")
            if Debug:
                print ("Switching off")
        elif ((mean_temp <= working_temp) and (mean_temp >= userreq_temp)):
#            e.g. Temp is 20.6
            send_call_boiler("on")
            if Debug:
                print ("Switching on")
        else:
             print ("Something gone wrong")
             if Debug:
                 print ("Switching Wrong")
    else:
        sleep(int(rotation_time/10))
        if Debug:
           print ("Sleeping %i" % (rotation_time/10))
        #We are in the loop but can sleep until ttl<35

if __name__ == "__main__":
   #Sleep on startup as redis needs to be online first
   sleep(10)
   while True:
       if Debug:
          print ("Looping")
       read_temps() 
       update_relayinfo()
       send_call_water()
       sleep(1)
   
