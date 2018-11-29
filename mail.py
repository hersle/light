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
import subprocess
from email.mime.text import MIMEText

def mail(recipient, subject, text):
    msg = MIMEText(text, "html")
    msg["To"] = recipient
    msg["Subject"] = subject
    try:
        subprocess.run(["/usr/sbin/sendmail", "-t", "-oi"], input=msg.as_bytes(), check=True)
        logging.info("mailed \"%s...\" to %s", subject[:7], (recipient.split("@")[0][:3] + "...@" + recipient.split("@")[1]))
    except Exception as e:
        logging.error("could not \"%s...\" to %s", subject[:7], (recipient.split("@")[0][:3] + "...@" + recipient.split("@")[1]))
        logging.error(str(e))

def notify():
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

    recipients = []
    file = open("subscribers", "r")
    for line in file:
        email = line.strip()
        mail(email, subject, text)
    file.close()

def createconfirmationcode():
    # random string
    code = ""
    for i in range(0, 30):
        code += random.choice(string.ascii_lowercase)
    return code
