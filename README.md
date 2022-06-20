# "Lysloggen"

Lysloggen er et idiotprosjekt for å måle mønsteret i tidspunktet der lyset i Realfagbygget på NTNU slukker automatisk.
Hver dag slukker lyset omtrent 0.75 sekunder senere enn dagen før, og tilsynelatende nullstilles slukkesystemet av og til for å holde dette tidspunktet mellom 19:40-20:00.
Det sekundære formålet er å gni inn skammen over å jobbe på Gløshaugen så sent på kvelden ved å trykke på en knapp *nøyaktig* idet lyset slukker.

## Tjenere

| Fra | Til | Nettadresse | Drifter |
|-----|-----|-------------|---------|
| 2018 | 2022 | ~~[folk.ntnu.no/hermasl/light/](https://folk.ntnu.no/hermasl/light/)~~  | Herman Sletmoen |
| 2022 | nå   |   [folk.ntnu.no/simonweg/light/](https://folk.ntnu.no/simonweg/light/)  | Simon Wego      |

## Bruksanvisning

### Oppsett

1. Åpne et terminalvindu:
	* Hvis du bruker Windows, åpne for eksempel programmet **Ledetekst**.
	* Hvis du bruker Mac, åpne for eksempel programmet **Terminal**.
	* Hvis du bruker Linux, vet du sannsynligvis selv hva du skal gjøre.
2. Logg inn på området ditt hos NTNUs Linux-webserver med `ssh DITT-NTNU-BRUKERNAVN@login.stud.ntnu.no` og NTNU-passordet ditt.
3. Skriv `cd public_html/` for å gå inn i mappen som inneholder filer som offentliggjøres under [folk.ntnu.no/DITT-NTNU-BRUKERNAVN](http://folk.ntnu.no/DITT-NTNU-BRUKERNAVN).
4. Skriv `https://github.com/hersle/light.git` for å laste ned kjernefunksjonaliteten til lysloggen fra dette GitHub-prosjektet.
5. Gå inn i mappen som nettopp ble lastet ned med `cd light/` og skriv deretter `ls -l` for å få oversikt over innholdet der.
6. **En tom lyslogg (uten målinger og epost-abonnenter) skal nå være tilgjengelig på  [folk.ntnu.no/DITT-NTNU-BRUKERNAVN/light](http://folk.ntnu.no/DITT-NTNU-BRUKERNAVN/light).**
7. Kopiér målinger fra en eksisterende lyslogg med for eksempel `wget http://folk.ntnu.no/hermasl/light/light.dat`.
8. Kopiér abonnenter fra en eksisterende lyslogg med for eksempel `wget --user="" --password="PASSWORD" http://folk.ntnu.no/hermasl/light/subscribers` hvis du kjenner passordet `PASSWORD`.
9. **Hvis du har gjort de siste skrittene, er lysloggen nå en eksakt kopi inkludert målinger og epost-abonnenter av den du har kopiert.**
