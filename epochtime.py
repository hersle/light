#!/usr/bin/python3

import datetime
import sys

if len(sys.argv) != 2:
    print("file not specified")
    exit()

file = open(sys.argv[1])
for line in file:
    datestr = line.strip()
    time = datetime.datetime.strptime(datestr, "%d.%m.%y %H:%M:%S")
    millis = int(time.timestamp() * 1000)
    print(millis)
file.close()
