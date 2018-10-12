<!DOCTYPE html>

<html>

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">

<link href="style.css" rel="stylesheet">

<body>

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

<script type="text/javascript">
	var req = new XMLHttpRequest();
	function sendSubscription () {
		req.open("POST", "subscription.php", false);
		req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		req.onreadystatechange = function() {
			console.log(req.readyState, req.status, "\"", req.response, "\"");
		};
		let str = document.getElementById("emailinput").value;
		req.send(encodeURI("email=" + "\"" + str + "\""));
	}
</script>

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

<script type="text/javascript">
	let stime = new Date(<?php echo microtime(true) * 1000 ?>);
	let ctime = new Date();
	let offset = stime.getTime() - ctime.getTime();
	let prediction = new Date(<?php echo shell_exec("python3 light.py 2>&1") ?>);
	document.getElementById("prediction").innerHTML = timeString(prediction, true);
	function pad2(n) {
		if (n < 10) {
			return "0" + n;
		} else {
			return n;
		}
	}
	function pad3(n) {
		if (n < 100) {
			return "0" + pad2(n);
		} else {
			return n;
		}
	}
	function timeString(dt, incl_ms) {
		let h = pad2(dt.getHours());
		let m = pad2(dt.getMinutes());
		let s = pad2(dt.getSeconds());
		let ms = pad3(dt.getMilliseconds());
		if (incl_ms) {
			return h + ":" + m + ":" + s + "." + ms;
		} else {
			return h + ":" + m + ":" + s;
		}
	}
	function dateString(dt, fully) {
		let d = pad2(dt.getDate());
		let m = pad2(dt.getMonth() + 1);
		let y = pad2(dt.getFullYear());
		if (!fully) {
			y = y % 100;
		}
		return d + "." + m + "." + y;
	}
	function updateTimer() {
		ctime = new Date();
		stime = new Date(ctime.getTime() + offset);

		document.getElementById("stime").innerHTML = timeString(stime, 1);
		document.getElementById("sdate").innerHTML = dateString(stime, 1);

		if (document.getElementById("updatebutton").style.backgroundColor == "grey") {
		} else if (Math.abs(stime - prediction) <= 30000) {
			document.getElementById("updatebutton").style.backgroundColor = "green";
		} else {
			document.getElementById("updatebutton").style.backgroundColor = "red";
			document.getElementById("updatebutton").innerHTML = "Lysregistrering åpner om " + Math.floor(((prediction - 30000) - stime) / 1000) + " sekunder";
		}
	}
	updateTimer();
	setInterval(updateTimer, 101);

	var xhr = new XMLHttpRequest();
	function updateServer () {
		xhr.open("POST", "post.php", false);
		xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4 && xhr.response === "Registrert.") {
				//console.log(xhr.readyState, xhr.status, xhr.response);
				location.reload();
				//document.getElementById("errormessage").innerHTML = "success";
			} else {
				console.log(xhr.readyState, xhr.status, "\"", xhr.response, "\"");
				document.getElementById("errormessage").innerHTML = xhr.response;
			}
		};
		let str = dateString(stime, 0) + " " + timeString(stime, 0);
		xhr.send(encodeURI("time=" + "\"" + str + "\""));
	}
	//updateServer();
</script>

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
