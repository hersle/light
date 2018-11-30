#!/usr/bin/python3

import datetime

def read_times():
    times = []
    file = open("light.dat", "r")
    for line in file:
        time = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n")
        times.append(time)
    file.close()
    return times

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

def get_prediction():
    epoch = datetime.datetime.utcfromtimestamp(0)
    x = []
    y = []
    for time in read_times():
        days = (time - epoch).days
        secs = (time - epoch).total_seconds()
        x.append(days)
        y.append(secs)

    a, b = linear_regression(x, y)

    today = datetime.datetime.today()
    days = (today - epoch).days
    secs = a * days + b
    time_prediction = datetime.datetime.utcfromtimestamp(secs)
    return time_prediction

def time_is_reasonable(time):
    prediction = get_prediction()
    return abs((time - prediction).total_seconds()) <= 30
