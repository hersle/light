#!/usr/bin/python3

import sys
import re
import datetime
import smtplib
import time
import random
import string
import measure
from email.mime.text import MIMEText

args = ["", "", ""]
for i in range(0, min(len(args), len(sys.argv[1:]))):
    args[i] = sys.argv[1+i]

if args[0] == "" or args[0] == "predict":
    epoch = datetime.datetime.utcfromtimestamp(0)
    print(int(measure.getprediction().timestamp() * 1000))
elif args[0] == "add":
    # add new time
    now = datetime.datetime.now()
    if measure.registered(now):
        print("Lys allerede registrert.")
    elif not measure.timeisreasonable(now):
        print("Ufysikalsk tid. For stort avvik.")
    else:
        print("Registrert.")
        file = open("light.dat", "a")
        line = now.strftime("%d.%m.%y %H:%M:%S\n")
        file.write(line)
        file.close()
elif args[0] == "open":
    now = datetime.datetime.now()
    if measure.registered(now):
        print("no")
    else:
        print("yes")
elif args[0] == "list":
    file = open("light.dat", "r")
    epoch = datetime.datetime.utcfromtimestamp(0)
    for line in file:
        time = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n")
        millis = int((time - epoch).total_seconds() * 1000)
        print(millis)
    file.close()
elif args[0] == "time":
    print(int(time.time() * 1000))
else:
    print("Ukjent kommando.")
