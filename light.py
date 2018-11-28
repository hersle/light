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
    logging.basicConfig(filename=logfilename, level=logminlevel, format=logformat)

    args = ["", "", ""]
    for i in range(0, min(len(args), len(sys.argv[1:]))):
        args[i] = sys.argv[1+i]

    logging.info("called with arguments %s", args)

    if args[0] == "" or args[0] == "predict":
        epoch = datetime.datetime.utcfromtimestamp(0)
        ms = int(measure.getprediction().timestamp() * 1000)
        print(ms)
        logging.info("predicted lights out at %d", ms)
    elif args[0] == "add":
        # add new time
        now = datetime.datetime.now()
        if measure.registered(now):
            print("Lys allerede registrert.")
            logging.info("not registered - already registered")
        elif not measure.timeisreasonable(now):
            print("Ufysikalsk tid. For stort avvik.")
            logging.info("not registered - too large difference from prediction")
        else:
            print("Registrert.")
            file = open("light.dat", "a")
            line = now.strftime("%d.%m.%y %H:%M:%S\n")
            file.write(line)
            file.close()
            logging.info("successfully registered lights out at %s on machine \"%s\"", line.strip(), os.popen("uname -a").read().split()[1])
    elif args[0] == "open":
        now = datetime.datetime.now()
        if measure.registered(now):
            print("no")
            logging.info("already registered")
        else:
            print("yes")
            logging.info("light not registered")
    elif args[0] == "list":
        file = open("light.dat", "r")
        epoch = datetime.datetime.utcfromtimestamp(0)
        for line in file:
            time = datetime.datetime.strptime(line, "%d.%m.%y %H:%M:%S\n")
            millis = int((time - epoch).total_seconds() * 1000)
            print(millis)
        file.close()
        logging.info("succesfully listed previous measurements")
    elif args[0] == "time":
        ms = int(time.time() * 1000)
        print(ms)
        logging.info("server time: %s ms (%s UTC) after epoch from \"%s\"", ms, datetime.datetime.utcfromtimestamp(int(ms / 1000)), os.popen("uname -a").read().split()[1])
    elif args[0] == "notify":
        mail.notify()
    elif args[0] == "subscribe":
        email = args[1]

        logging.info("received subscription request from %s", email)

        # validate email
        if not re.match("[^@]+@[^@]+\.[^@]+", email) or email.split()[0] != email:
            print("Ugyldig formatert epostadresse.")
            logging.info("denied subscription request - format error")
            exit()

        random.seed(time.time())
        code = createconfirmationcode()
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
        mail([email], subject, text)
        print("En bekreftelsesepost er sendt til " + email + ".")
        logging.info("processed subscription request, attempted to send confirmation email")
    elif args[0] == "confirm":
        email = args[1]
        code = args[2]

        logging.info("received subscription confirmation request from %s", email)

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
            logging.info("successfully confirmed subscription")
        else:
            print(email + " ikke bekreftet.")
            logging.info("subscription not confirmed - email not found or incorrect code")
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
