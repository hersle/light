#!/usr/bin/python3

import sys
import os
import datetime
import time
import measure
import logging
import mail

def initialize_log():
    name = os.uname().nodename
    pid = os.getpid()
    filename = "log"
    minlevel = logging.DEBUG
    format = "%%(asctime)s @ %s-%05d: (%%(levelname)s) %%(message)s" % (name, pid)
    handler = logging.FileHandler(filename, "a", "utf-8")
    logging.basicConfig(level=minlevel, format=format, handlers=[handler])

if __name__ == "__main__":
    initialize_log()

    args = ["", "", ""]
    for i in range(0, min(len(args), len(sys.argv[1:]))):
        args[i] = sys.argv[1+i]

    logging.info("executing \"%s\"", " ".join(sys.argv))

    if args[0] == "predict":
        ms = int(measure.get_prediction().timestamp() * 1000)
        print(ms)
    elif args[0] == "add":
        # add new time
        now = datetime.datetime.now()
        if not measure.time_is_available(now):
            print("Lys allerede registrert.")
            logging.info("denied registration due to earlier registration today")
        elif not measure.time_is_reasonable(now):
            print("Ufysikalsk tid. For stort avvik.")
            logging.info("denied registration due to large deviation from prediction")
        else:
            measure.add_time(now)
            print("Registrert.")
            logging.info("successfully registered")
    elif args[0] == "open":
        now = datetime.datetime.now()
        if measure.time_is_available(now):
            print("yes")
        else:
            print("no")
    elif args[0] == "list":
        epoch = datetime.datetime.utcfromtimestamp(0)
        times = measure.read_times()
        for time in times:
            millis = int((time - epoch).total_seconds() * 1000)
            print(millis)
    elif args[0] == "time":
        ms = int(time.time() * 1000)
        print(ms)
    elif args[0] == "notify":
        mail.notify()
    elif args[0] == "subscribe":
        email = args[1]

        if not mail.is_valid_email(email):
            print("Ugyldig formatert epostadresse.")
            logging.info("denied subscription from %s due to format error", email)
            exit()

        if mail.is_subscribed(email):
            print("Epostadressen er allerede registrert.")
            logging.info("denied second subscription request from %s", email)
            exit()

        mail.add_subscriber(email)
    elif args[0] == "confirm":
        email = args[1]
        code = args[2]
        mail.confirm_subscription(code, email)
    elif args[0] == "unsubscribe":
        print("Stengt.")
        exit()

        email = args[1]

        file = open("subscribers", "r")
        lines = file.readlines()
        file.close()

        found = False
        file = open("subscribers", "w")
        # TODO: could potentially delete all subscribers upon error
        for line in lines:
            words = line.split()
            if words[1] == email:
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
