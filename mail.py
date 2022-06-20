#!/usr/bin/python3

import re
import time
import random
import string
import logging
import subprocess
import email.mime.text

def mail(recipient, subject, text):
    msg = email.mime.text.MIMEText(text, "html")
    msg["From"] = "noreply@campusservice.ntnu.no"
    msg["To"] = recipient
    msg["Subject"] = subject

    try:
        cmd = ["/usr/sbin/sendmail", "-t", "-oi"]
        subprocess.run(cmd, input=msg.as_bytes(), check=True)
    except Exception as e:
        logging.error("could not mail \"%s...\" to %s", subject, anonymize_email(recipient))
        logging.error(str(e))
        return

    logging.info("mailed \"%s...\" to %s", subject[:7], anonymize_email(recipient))

def is_valid_email(email):
    return re.fullmatch("[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

def anonymize_email(email):
    if not is_valid_email(email):
        return "INVALIDEMAIL"
    index_at = email.find("@")
    if index_at >= 3:
        return email[:3]        + "..." + email[index_at:] # e.g. abcdef@ntnu.no -> abc...@ntnu.no
    else:
        return email[:index_at] + "..." + email[index_at:] # e.g. ab@ntnu.no -> ab...@ntnu.no

def read_subscribers(confirmed=True):
    subscribers = []
    filename = "subscribers" if confirmed else "subscribers_unconfirmed"
    file = open(filename, "r")
    for line in file:
        words = line.split()
        code = words[0]
        email = words[1]
        subscribers.append((code, email))
    file.close()
    return subscribers

def read_subscribers_email(confirmed=True):
    emails = []
    subscribers = read_subscribers(confirmed)
    for subscriber in subscribers:
        email = subscriber[1]
        emails.append(email)
    return emails

def write_subscribers(subscribers, confirmed=True):
    filename = "subscribers" if confirmed else "subscribers_unconfirmed"
    file = open(filename, "w")
    for subscriber in subscribers:
        code = subscriber[0]
        email = subscriber[1]
        line = code + " " + email + "\n"
        file.write(line)
    file.close()

def is_subscribed(email):
    return email in read_subscribers_email()

def add_subscriber(email):
    code = create_confirmation_code()
    subscriber = (code, email)

    subscribers = read_subscribers(confirmed=False)
    subscribers.append(subscriber)
    if len(subscribers) >= 1000: # keep at most 1000 last subscription requests
        subscribers = subscribers[len(subscribers)-1000:]
    write_subscribers(subscribers, confirmed=False)

    link = "http://folk.ntnu.no/hermasl/light/confirm_subscription.php"
    link += "?email=" + email + "&code=" + code

    subject = "Bekreftelse av varsling ved måling av lysslukking"
    text = ""
    text += "\"" + email + "\" har anmodet om å motta varsler hver gang lysslukking på Fysikkland måles.\n"
    text += "For å bekrefte abonnementet, klikk <a href=\"" + link + "\">her</a>.\n"
    mail(email, subject, text)
    print("En bekreftelsesepost er sendt til " + email + ".")
    logging.info("received subscription request from %s", email)

def confirm_subscription(code, email):
    subscribers_unconfirmed = read_subscribers(confirmed=False)

    for i, subscriber in enumerate(subscribers_unconfirmed):
        if email == subscriber[1] and code == subscriber[0]:
            subscribers_unconfirmed.pop(i)
            write_subscribers(subscribers_unconfirmed, confirmed=False)

            subscribers = read_subscribers()
            subscribers.append(subscriber)
            write_subscribers(subscribers)

            print(email + " bekreftet.")
            logging.info("confirmed subscription from %s", email)
            return

    print(email + " ikke bekreftet.")
    logging.info("failed to confirm subscription from %s", email)

def confirm_unsubscription(code, email):
    subscribers = read_subscribers()

    for i, subscriber in enumerate(subscribers):
        if email == subscriber[1] and code == subscriber[0]:
            subscribers.pop(i)
            write_subscribers(subscribers)

            print("Avsluttet abonnement for %s." % email)
            logging.info("unsubscribed %s", email)
            return

    print("Kunne ikke avslutte abonnement for %s." % email)
    logging.info("failed to unsubscribe from %s", email)

def notify():
    subject = "Noen målte nettopp lyset på Fysikkland!"

    text_common = ""
    text_common += "Navigér til <a href=\"http://folk.ntnu.no/hermasl/light\">folk.ntnu.no/hermasl/light</a> for å se målingen!\n"
    text_common += "\n"
    text_common += "Som medlem av Fysikklandlysets epostliste bidrar du til sikker arkivering av lysloggen gjennom et distribuert blockchain-inspirert sikkerhetskopieringssystem.\n"
    text_common += "Du vil derfor finne en kopi av lysloggen under.\n"
    text_common += "Fysikkland anmoder deg om å ta godt vare på kopien i tilfelle noe ufysikalsk inntreffer og den sentrale loggen tilintetgjøres helt eller delvis.\n"
    text_common += "\n"
    text_common += "Fysikkland ønsker deg en fin dag videre.\n"
    text_common += "\n"
    text_common += "--- START LYSLOGG SIKKERHETSKOPI ---\n"
    file = open("light.dat", "r")
    for line in file:
        text_common += line
    file.close()
    text_common += "--- SLUTT LYSLOGG SIKKERHETSKOPI ---\n"

    for subscriber in read_subscribers():
        code = subscriber[0]
        recipient = subscriber[1]
        link = "http://folk.ntnu.no/hermasl/light/unsubscribe.php"
        link += "?email=" + recipient + "&code=" + code
        text_unique = "Dersom du ikke lenger ønsker å varsles når lysslukkingen på Fysikkland registreres, kan du avslutte ditt abonnement <a href=\"%s\">her</a>." % link

        text = text_common + "\n" + text_unique
        text = text.replace("\n", "<br>")

        mail(recipient, subject, text)

def create_confirmation_code():
    random.seed(time.time())
    code = ""
    for i in range(0, 30):
        code += random.choice(string.ascii_lowercase)
    return code
