#!/usr/bin/python3

import datetime

def read_times():
    times = []
    file = open("light.dat", "r")
    for line in file:
        if not line.startswith("JUMP "):
            time = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n")
            times.append(time)
    file.close()
    return times

def read_jumps():
    jumps = []
    file = open("light.dat", "r")
    for line in file:
        if line.startswith("JUMP "):
            _, date, jump = line.split(" ")
            date = datetime.datetime.strptime(date, "%d.%m.%y")
            jump = int(jump)
            jumps.append((date, jump))
    file.close()
    return jumps

def add_time(time):
    line = time.strftime("%d.%m.%y %H:%M:%S\n")
    file = open("light.dat", "a")
    file.write(line)
    file.close()

def linear_regression(x, y):
    assert len(x) == len(y), "different number of x and y values"
    n = len(x)
    sx, sy, sxx, sxy, syy = 0, 0, 0, 0, 0
    for i in range(0, n):
        sx += x[i]
        sy += y[i]
        sxx += x[i] * x[i]
        sxy += x[i] * y[i]
        syy += y[i] * y[i]
    a = (n * sxy - sx * sy) / (n * sxx - sx**2)
    b = (sy * sxx - sx * sxy) / (n * sxx - sx**2)
    return a, b

def time_is_available(time):
    date = time.date()
    for time in read_times():
        if (time.date() - date).days == 0:
            return False
    return True

def get_prediction(date=datetime.datetime.today()):
    epoch = datetime.datetime.utcfromtimestamp(0)
    x = []
    y = []
    jumps = read_jumps()
    for time in read_times():
        if time >= date:
            break
        # subtract jumps from measurements,
        # predicting as if all points lie on a straight line
        for jumpdate, jumpms in jumps:
            if time >= jumpdate and jumpdate <= date:
                time = time - datetime.timedelta(milliseconds=jumpms) # predict as if one continuous straight line
        days = (time - epoch).days
        secs = (time - epoch).total_seconds()
        x.append(days)
        y.append(secs)

    if len(x) < 2:
        return None

    a, b = linear_regression(x, y)

    today = datetime.datetime.today()
    days = (date - epoch).days
    secs = a * days + b
    # add jumps to prediction
    for jumpdate, jumpms in jumps:
        if time >= jumpdate and jumpdate <= date:
            secs = secs + jumpms / 1000 # sawtooth
    time_prediction = datetime.datetime.utcfromtimestamp(secs)
    return time_prediction

def time_is_reasonable(time):
    prediction = get_prediction()
    return abs((time - prediction).total_seconds()) <= 30
