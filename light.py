#!/usr/bin/python3

import sys
import re
import datetime
import smtplib
import time
import random
from email.mime.text import MIMEText

args = ["", ""]
for i in range(0, min(len(args), len(sys.argv[1:]))):
    args[i] = sys.argv[1+i]

def mail(recipients, subject, text):
    fromaddr = "fysikklandlyset@mail.com"
    password = "Fysikkland123"
    smtpaddr = "smtp.mail.com"
    port = 587

    server = smtplib.SMTP()
    server.connect(smtpaddr, port)
    server.login(fromaddr, password)

    msg = MIMEText(text)
    msg["From"] = fromaddr
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    try:
        server.send_message(msg)
    except Exception as e:
        print(e)
        exit()

    server.quit()

def notify():
    recipients = []
    file = open("subscribers", "r")
    for line in file:
        email = line.strip()
        recipients.append(email)
    file.close()

    subject = "Noen målte nettopp lyset på Fysikkland!"

    text = ""
    text += "Navigér til http://folk.ntnu.no/hermasl/light for å se målingen!\n"
    text += "\n"
    text += "Som medlem av Fysikklandlysets epostliste bidrar du til sikker arkivering av lysloggen gjennom et distribuert blockchain-inspirert sikkerhetskopieringssystem.\n"
    text += "Du vil derfor finne en kopi av lysloggen under.\n"
    text += "Fysikkland anmoder deg om å ta godt vare på kopien i tilfelle noe ufysikalsk inntreffer og den sentrale loggen tilintetgjøres helt eller delvis.\n"
    text += "\n"
    text += "Fysikkland ønsker deg en fin dag videre.\n"
    text += "\n"
    text += "--- START LYSLOGG SIKKERHETSKOPI ---\n"
    file = open("light.dat", "r")
    for line in file:
        text += line
    file.close()
    text += "--- SLUTT LYSLOGG SIKKERHETSKOPI ---\n"

    mail(recipients, subject, text)

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
    if not timeisreasonable(now):
        print("Ufysikalsk tid. For stort avvik.")
    elif registered(now):
        print("Lys allerede registrert.")
    else:
        print("Registrert.")
        file = open("light.dat", "a")
        line = now.strftime("%d.%m.%y %H:%M:%S\n")
        file.write(line)
        file.close()
        notify()
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
elif args[0] == "subscribe":
    print("Epostregistrering stengt.")
    exit()

    random.seed(time.time())
    email = args[1]
    code = random.randint(1, 9999999999)
    file = open("subscribers_unconfirmed", "a")
    line = str(code) + " " + email + "\n"
    file.write(line)
    file.close()
else:
    print("Ukjent kommando.")
