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

function updatePrediction() {
	document.getElementById("prediction").innerHTML = timeString(prediction, true);
}

function timeString(dt, incl_ms) {
	let h = String(dt.getHours()).padStart(2, "0");
	let m = String(dt.getMinutes()).padStart(2, "0");
	let s = String(dt.getSeconds()).padStart(2, "0");
	let ms = String(dt.getMilliseconds()).padStart(3, "0");
	if (incl_ms) {
		return h + ":" + m + ":" + s + "." + ms;
	} else {
		return h + ":" + m + ":" + s;
	}
}
function dateString(dt, fully) {
	let d = String(dt.getDate()).padStart(2, "0");
	let m = String(dt.getMonth() + 1).padStart(2, "0");
	let y = String(dt.getFullYear()).padStart(2, "0");
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
setInterval(updateTimer, 101);

var xhr = new XMLHttpRequest();
function updateServer () {
	xhr.open("POST", "post.php", false);
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.response === "Registrert.") {
			location.reload();
		} else {
			console.log(xhr.readyState, xhr.status, "\"", xhr.response, "\"");
			document.getElementById("errormessage").innerHTML = xhr.response;
		}
	};
	xhr.send();
}
