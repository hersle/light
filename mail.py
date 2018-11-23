#!/usr/bin/python3

import os
import sys
import re
import datetime
import smtplib
import time
import random
import string
import logging
from email.mime.text import MIMEText

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
        logging.info("successfully sent email \"%s...\" to %s", subject[:7], [",".join([(email.split("@")[0][:3] + "...@" + email.split("@")[1]) for email in recipients])])
    except Exception as e:
        print(e)
        logging.error("could not send email \"%s...\" to %s: %s", subject[:7], [",".join([(email.split("@")[0][:3] + "...@" + email.split("@")[1]) for email in recipients])], e)
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
    text += "Navigér til <a href=\"http://folk.ntnu.no/hermasl/light\">folk.ntnu.no/hermasl/light</a> for å se målingen!\n"
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
    text = text.replace("\n", "<br>")

    mail(recipients, subject, text)

def createconfirmationcode():
    # random string
    code = ""
    for i in range(0, 30):
        code += random.choice(string.ascii_lowercase)
    return code
