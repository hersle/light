#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText

fromaddr = "fysikklandlyset@mail.com"
toaddr = "hermansletmoen@gmail.com"
password = "Fysikkland123"
smtpaddr = "smtp.mail.com"
port = 587

server = smtplib.SMTP()
server.connect(smtpaddr, port)
server.login(fromaddr, password)

msg = MIMEText("testepost")
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = "Fysikklandlyset"
server.send_message(msg)

server.quit()
