#!/usr/bin/python
import re

def convert_time(instring):
    mytime = re.compile(r'(\d+)(\w)$')
    mytime.findall(instring)
    digits=int(mytime.findall(instring)[0][0])
    timeunits=mytime.findall(instring)[0][1]
    print(f'Digits = {digits}')
    print(f'Timeunits = {timeunits}')
    if timeunits == "h":
        multiple=3600
    elif timeunits == "m":
        multiple=60
    elif timeunits == "d":
        multiple=81400
    else:
        multiple=1
    total_time = int(digits*multiple)
    return (total_time)


#total_time=convert_time("60m")
#print (f'Total time = {total_time}')
#total_time=convert_time("1h")
#print (f'Total time = {total_time}')
#total_time=convert_time("365d")
#print (f'Total time = {total_time}')

