#!/usr/bin/python3

import mail

# usage: set recipients, subject and text, then run this script to send email

#recipients = mail.read_subscribers_email() # uncomment to send to all subscribers
recipients = ["hermansletmoen@gmail.com"] # uncomment to send to myself for testing

subject = "Oppdatering om for- og fremtiden fra Fysikkland"
text = """Kjære lysslukker,<br>
<br>
Fysikklands tjeneste for måling av tidspunkt for slukking av lys har dessverre vært utilgjengelig en kort periode.
Situasjonen skyldes en uforsvarlig og tilsynelatende manuell intervensjon fra NTNU Driftsavdelingen i systemet for slukking av lys som endret slukketidspunktet med 20 minutter og 4 sekunder.
Tjenestens utviklingsteam har jobbet på spreng for å håndtere avviket og kan nå rapportere om at <a href="https://folk.ntnu.no/hermasl/light/">tjenesten</a> nå er tilgjengelig for bruk igjen.
På vegne av NTNU Driftsavdelingen beklages eventuelle ulemper dette har medført.
<br><br>
Det rettes en stor takk til Jonas Bueie for måling av det avvikende og legendariske slukketidspunktet 5. mars 2020 klokken 20:01:13.
Til tross for sjokket som oppsto da lyset ikke slukket til estimert tidspunkt denne kvelden, fortsatte Bueie å stirre uproduktivt og intensivt på klokken i over 20 minutter, før han noterte seg det nøyaktige slukketidspunktet 20:01:13 uten så mye som å blunke.
Fysikkland kan bekrefte at korreksjon for den over to år gamle målingen estimerer nøyaktige slukketidspunkter den dag i dag.
Den aktuelle målingen vil heretter refereres til som "den legendariske Bueie-målingen", og dens måler utnevnes herved til <b>Målemester Jonas Bueie</b>.
<br><br>
Det har kommet til Fysikklands oppmerksomhet at Thorvald Ballestad har kopiert lysloggen til sin egen hjemmeside og drevet omfattende promotering av <a href="https://folk.ntnu.no/thorvalb/light/">den konkurrerende tjenesten</a>.
Fysikkland anmoder Ballestad om å legge ned sin piratvirksomhet, og anbefaler alle om å benytte <a href="https://folk.ntnu.no/hermasl/light/">den opprinnelige tjenesten</a>.
<br><br>
Grunnet fullførte studier ser Fysikkland nå etter en arvtaker som kan overta driften av lysmonitoreringstjenesten på sin folk.ntnu-hjemmeside, og eventuelt videreutvikle den etter eget ønske.
Interesserte bes om å ta kontakt med Fysikkland.
<br><br>
Fysikkland ønsker deg en fortsatt fin dag og lykke til med fullføringen av eventuelt gjenstående studier.
"""

for recipient in recipients:
    mail.mail(recipient, subject, text)
    print("Mailed %s<br>" % recipient)
