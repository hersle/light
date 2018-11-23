#!/usr/bin/python3

import sys
import re
import datetime
import smtplib
import time
import random
import string
from email.mime.text import MIMEText

args = ["", "", ""]
for i in range(0, min(len(args), len(sys.argv[1:]))):
    args[i] = sys.argv[1+i]

def linregr(x, y):
        assert len(x) == len(y), "different number of x and y values"
        n = len(x)
        sx, sy = sum(x), sum(y)
        sxx, sxy, syy = sum(x**2 for x in x), sum(x * y for x, y in zip(x, y)), sum(y**2 for y in y)
        delta  = n * sxx - sx**2
        a = (n * sxy - sx * sy) / delta
        b = (sy * sxx - sx * sxy) / delta
        dy = [y - (a * x + b) for x, y in zip(x, y)]
        s = sum(dy**2 for dy in dy)
        da = (n * s / ((n - 2) * delta))**(1/2)
        db = (s * sxx / ((n - 2) * delta))**(1/2)
        # return a, b, da, db
        return a, b

def registered(time):
    file = open("light.dat", "r")
    today = time.date()
    reg = False
    for line in file:
        date = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n").date()
        if (date - today).days == 0:
            reg = True
            break
    file.close()
    return reg

def getprediction():
    # print prediction for today
    epoch = datetime.datetime.utcfromtimestamp(0)
    file = open("light.dat", "r")
    x = []
    y = []
    for line in file:
        time = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n")
        days = (time - epoch).days
        secs = (time - epoch).total_seconds()
        x.append(days)
        y.append(secs)
    file.close()

    a, b = linregr(x, y)

    time = datetime.datetime.today()
    days = (time - epoch).days
    secs = a * days + b
    time = datetime.datetime.utcfromtimestamp(secs)
    return time

def timeisreasonable(time):
    prediction = getprediction()
    return abs((time - prediction).total_seconds()) <= 30

def log(str):
    file = open("log", "a")
    line = str + "\n"
    file.write(line)
    file.close()

if args[0] == "" or args[0] == "predict":
    epoch = datetime.datetime.utcfromtimestamp(0)
    print(int(getprediction().timestamp() * 1000))
elif args[0] == "add":
    # add new time
    now = datetime.datetime.now()
    if registered(now):
        print("Lys allerede registrert.")
    elif not timeisreasonable(now):
        print("Ufysikalsk tid. For stort avvik.")
    else:
        print("Registrert.")
        file = open("light.dat", "a")
        line = now.strftime("%d.%m.%y %H:%M:%S\n")
        file.write(line)
        file.close()
elif args[0] == "open":
    now = datetime.datetime.now()
    if registered(now):
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
