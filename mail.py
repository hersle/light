#!/usr/bin/python3

import os
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

def mail(recipients, subject, text):
    fromaddr = "fysikklandlyset@mail.com"
    password = "Fysikkland123"
    smtpaddr = "smtp.mail.com"
    port = 587

    server = smtplib.SMTP()
    server.connect(smtpaddr, port)
    server.login(fromaddr, password)

    msg = MIMEText(text, "html")
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

def createconfirmationcode():
    # random string
    code = ""
    for i in range(0, 30):
        code += random.choice(string.ascii_lowercase)
    return code

if args[0] == "notify":
    notify()
elif args[0] == "subscribe":
    email = args[1]

    # validate email
    if not re.match("[^@]+@[^@]+\.[^@]+", email) or email.split()[0] != email:
        print("Ugyldig formatert epostadresse.")
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
    else:
        print(email + " ikke bekreftet.")
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
