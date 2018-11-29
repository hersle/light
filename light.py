#!/usr/bin/python3

import sys
import os
import re
import datetime
import smtplib
import time
import random
import string
import measure
import logging
import mail
from email.mime.text import MIMEText

if __name__ == "__main__":
    machinename = os.popen("uname -a").read().split()[1]
    pid = "%05d" % os.getpid()
    logfilename = "log"
    logminlevel = logging.DEBUG
    logformat = "%(asctime)s @ " + machinename + "-" + pid + ": (%(levelname)s) %(message)s"
    logging.basicConfig(level=logminlevel, format=logformat, handlers=[logging.FileHandler(logfilename, "a", "utf-8")])

    args = ["", "", ""]
    for i in range(0, min(len(args), len(sys.argv[1:]))):
        args[i] = sys.argv[1+i]

    logging.info("executing \"%s\"", " ".join(sys.argv))

    if args[0] == "predict":
        epoch = datetime.datetime.utcfromtimestamp(0)
        ms = int(measure.getprediction().timestamp() * 1000)
        print(ms)
    elif args[0] == "add":
        # add new time
        now = datetime.datetime.now()
        if measure.registered(now):
            print("Lys allerede registrert.")
            logging.info("denied registration due to earlier registration today")
        elif not measure.timeisreasonable(now):
            print("Ufysikalsk tid. For stort avvik.")
            logging.info("denied registration due to large deviation from prediction")
        else:
            print("Registrert.")
            file = open("light.dat", "a")
            line = now.strftime("%d.%m.%y %H:%M:%S\n")
            file.write(line)
            file.close()
            logging.info("successfully registered")
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
        ms = int(time.time() * 1000)
        print(ms)
    elif args[0] == "notify":
        mail.notify()
    elif args[0] == "subscribe":
        email = args[1]

        # validate email
        if not re.match("[^@]+@[^@]+\.[^@]+", email) or email.split()[0] != email:
            print("Ugyldig formatert epostadresse.")
            logging.info("denied subscription from %s due to format error", email)
            exit()

        random.seed(time.time())
        code = mail.createconfirmationcode()
        file = open("subscribers_unconfirmed", "r")
        lines = file.readlines()
        line = code + " " + email + "\n"
        lines.append(line)
        if len(lines) >= 1000: # only keep 1000 most recent subscription requests
            lines = lines[len(lines)-1000:]
        file.close()
        file = open("subscribers_unconfirmed", "w")
        file.writelines(lines)
        file.close()

        link = "http://folk.ntnu.no/hermasl/light/confirm_subscription.php"
        link += "?email=" + email + "&code=" + code

        subject = "Bekreftelse av varsling ved måling av lysslukking"
        text = ""
        text += "\"" + email + "\" har anmodet om å motta varsler hver gang lysslukking på Fysikkland måles.\n"
        text += "For å bekrefte abonnementet, klikk <a href=\"" + link + "\">her</a>.\n"
        mail.mail(email, subject, text)
        print("En bekreftelsesepost er sendt til " + email + ".")
        logging.info("received subscription request from %s", email)
    elif args[0] == "confirm":
        email = args[1]
        code = args[2]

        file = open("subscribers_unconfirmed", "r")
        lines = file.readlines()
        file.close()

        file = open("subscribers_unconfirmed", "w")
        ok = False
        for line in lines:
            words = line.split()
            if email == words[1] and code == words[0]:
                ok = True
            else:
                file.write(line)
        file.close()

        if ok:
            file = open("subscribers", "a")
            line = email + "\n"
            file.write(line)
            file.close()
            print(email + " bekreftet.")
            logging.info("confirmed subscription from %s", email)
        else:
            print(email + " ikke bekreftet.")
            logging.info("failed to confirm subscription from %s", email)
    elif args[0] == "unsubscribe":
        print("Stengt.")
        exit()

        email = args[1]

        file = open("subscribers", "r")
        lines = file.readlines()
        file.close()

        found = False
        file = open("subscribers", "w")
        for line in lines:
            if line.strip() == email:
                found = True
            else:
                file.write(line)
        file.close()

        if found:
            print("Abonnementet til " + email + " er avsluttet.")
        else:
            print("Fant ikke " + email + ".")
    else:
        print("Ukjent kommando.")
