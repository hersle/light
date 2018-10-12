<!DOCTYPE html>

<html>

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">

<link href="style.css" rel="stylesheet">
<script type="text/javascript" src="javascript.js"></script>
<script type="text/javascript">
	var stime = new Date(<?php echo microtime(true) * 1000 ?>);
	var prediction = new Date(<?php echo shell_exec("python3 light.py 2>&1") ?>);
	var ctime = new Date();
	var offset = stime.getTime() - ctime.getTime();
</script>

<body onload="updatePrediction()">

<h1>Lyset på Fysikkland</h1>

<div class="announcement">
Fysikkland legger vekt på åpenhet i data.
Derfor er maskineriet bak lysloggen nå tilgjengelig på <a href="https://github.com/hersle/light">GitHub</a>.
Alle brukere oppfordres til å melde inn feil og sende inn forslag til forbedringer her!
</div>

<div class="announcement">
<strong>Nyhet: </strong>registrér deg for å motta varsler hver gang lyset på Fysikkland måles!
	<form>
	<label for="email">Epost:</label>
	<input id="emailinput" name="email" type="text"/>
	<button type="submit" onclick="sendSubscription()">Abonner</button>
	</form>
</div>

<table>
	<tr>
		<th>Dato</td>
		<td id="sdate"></td>
	</tr>
	<tr>
		<th>Servertid</td>
		<td id="stime"></td>
	</tr>
	<tr>
		<th>Estimert slukketid</th>
		<td id="prediction">
			<?php
			$output = shell_exec("python3 light.py 2>&1");
			echo "$output";
			?>
		</td>
	</tr>
</table>

<p id="errormessage"></p>

<form>
<?php
$ans = shell_exec("python3 light.py open");
if ($ans === "yes\n") {
	echo '<button id="updatebutton" onclick="updateServer()" type="button">Registrér lysslukking</button>';
} else {
	echo '<button id="updatebutton" style="background: grey;" disabled>Slukking allerede registrert</button>';
}
?>
</form>


<h2>Lyslogg</h2>

<table>
<tr><th>Dato</th><th>Klokkeslett</th></tr>
<?php
$lines = file("light.dat");
$lines = array_reverse($lines);
foreach ($lines as $line_num => $line) {
	$parts = preg_split("/\s+/", $line);
	$date = $parts[0];
	$time = $parts[1];
	echo "<tr><td>$date</td><td>$time</td></tr>";
}
?>

</table>

<h2>Om lyset på Fysikkland</h2>

<p>
Det kan vises empirisk at lyset på Fysikkland slukker automatisk hver dag i henhold til et systematisk mønster.
</p>
<p>
Registreringen av lysslukkingstidspunktene på Fysikkland er et samarbeidsprosjekt mellom Fysikkland og ingen andre for å utvikle digital kompetanse i det norske samfunnet, for å fremme det grønne skiftet og basere Norge på en bærekraftig og miljøvennlig økonomisk modell.
Denne nettsiden er et initiativ for å tilgjengeliggjøre og digitalisere måleprosessen, for å øke nøyaktigheten og andre fremmedord.
</p>


<h2>Hypotetisk forklaring</h2>

<p>
En plausibel forklaring på hvorfor lyset på Fysikkland slukker tidligere hver dag er gjengitt under.
Forklaringen forener de lenge adskilte teoriene om røykemannen og lyset og kalles derfor den universelle
Fysikklandsteorien.
</p>
<p>
Vi antar at det automatiske lysslukkesystemet er designet av rasjonelle agenter som opprinnelig
laget systemet slik at lyset slukket til nøyaktig samme tid hver dag. Fordi det er observert at lyset
slukker nøyaktig samtidig som på Fysikkland også i andre rom på NTNU, antar vi også at det finnes
en sentral lysslukkingsserver tilkoblet lysene som sender ut et signal via kabel til alle lysene som skal
slås av. Antagelsene krever at de rasjonelle agentene må ha tatt i betraktning selvinduktansen til dette
ledningssystemet, og derfor utviklet programvare som sender ut slukkesignalet noe før enn det som ville
krevdes med null selvinduktans, for å kompensere for den reduserte farten til signalet som følge av den
bremsende selvinduktansen.
</p>
<p>
Siden røykemannen røyker jevnlig, vil innholdet av aromatiske hydrokarboner i luften på Fysikkland
og Realfagsbygget øke jevnt over tid. De aromatiske hydrokarbonene har desentraliserte elektroner og
leder derfor strøm rundt i de sykliske forbindelsene. Derfor vil hver av disse forbindelsene fungere som en
magnetisk dipol. Når signalet fra slukkeserveren sendes ut til lysene gjennom ledninger, vil strømmene
i ledningene sette opp et magnetfelt som retter de magnetiske dipolene fra røyken motsatt vei av feltet
satt opp av ledningene. Dipolene svekker dermed det totale magnetiske feltet, og reduserer selvinduktan-
sen i ledningssystemet. De aromatiske hydrokarbonene emittert av røykemannen fungerer dermed som
magnetiske dipoler i et diamagnetisk materiale som svekker det totale magnetfeltet.
</p>
<p>
Resultatet blir at signalet fra slukkeserveren, som programvaren sender ut til nøyaktig samme tidspunkt hver dag, når frem til lysene tidligere enn det programvaren antar jo mer røykemannen har røyket,
slik at lyset slukkes tidligere.
</p>
<p>
Siden røykemannen røyker jevnlig, forklarer dette også at lysslukketidspunktet avtar lineært.
</p>
<p>
Dersom korrelasjonen mellom røyking og lysslukking observeres og bekreftes mange nok ganger, vil vi
med dette ifølge Hume bekrefte teorien så den garantert er sann. Fysikkland velger heller å sette sin lit
til Karl Popper og hans hypotetisk-deduktive metode. Derfor vil teorien utsettes for falsifiseringsforsøk
i tråd med hands metode, og en bedre forklaring vil fremsettes om nødvendig.
</p>


</body>


</html>
