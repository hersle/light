var offset = 0;

function sendSubscription () {
	var req = new XMLHttpRequest();
	req.open("POST", "subscribe.php");
	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.addEventListener("load", function() {
		console.log(req.readyState, req.status, "\"", req.response, "\"");
	});
	let str = document.getElementById("emailinput").value;
	req.send(encodeURI("email=" + "\"" + str + "\""));
}

function timeString(dt, incl_ms) {
	let h = String(dt.getHours()).padStart(2, "0");
	let m = String(dt.getMinutes()).padStart(2, "0");
	let s = String(dt.getSeconds()).padStart(2, "0");
	let str = h + ":" + m + ":" + s;
	if (incl_ms) {
		let ms = String(dt.getMilliseconds()).padStart(3, "0");
		str += "." + ms;
	}
	return str;
}
function dateString(dt) {
	let d = String(dt.getDate()).padStart(2, "0");
	let m = String(dt.getMonth() + 1).padStart(2, "0");
	let y = String(dt.getFullYear()).padStart(2, "0");
	return d + "." + m + "." + y;
}
function updateTimer() {
	ctime = new Date();
	stime = new Date(ctime.getTime() + offset);

	document.getElementById("stime").innerHTML = timeString(stime, true);
	document.getElementById("sdate").innerHTML = dateString(stime);

	if (document.getElementById("updatebutton").style.backgroundColor == "grey") {
	} else if (Math.abs(stime - prediction) <= 30000) {
		document.getElementById("updatebutton").style.backgroundColor = "green";
	} else {
		document.getElementById("updatebutton").style.backgroundColor = "red";
		document.getElementById("updatebutton").innerHTML = "Lysregistrering åpner om " + Math.floor(((prediction - 30000) - stime) / 1000) + " sekunder";
	}
}

function pollServerTime() {
	var req = new XMLHttpRequest();
	req.open("GET", "time.php");
	req.addEventListener("load", function() {
		let secondsUTC = req.response;
		stime = new Date(parseInt(secondsUTC));
		ctime = new Date();
		offset = stime.getTime() - ctime.getTime();
	});
	req.send();
}

function getPrediction() {
	var req = new XMLHttpRequest();
	req.open("GET", "prediction.php");
	req.addEventListener("load", function() {
		let secondsUTC = req.response;
		prediction = new Date(parseInt(secondsUTC));
		console.log("pred:", prediction);
		document.getElementById("prediction").innerHTML = timeString(prediction, true);
	});
	req.send();
}


function updateServer () {
	var req = new XMLHttpRequest();
	req.open("POST", "post.php");
	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.addEventListener("load", function() {
		if (req.readyState == 4 && req.response === "Registrert.") {
			location.reload();
		} else {
			console.log(req.readyState, req.status, "\"", req.response, "\"");
			document.getElementById("errormessage").innerHTML = req.response;
		}
	});
	req.send();
}

window.addEventListener("load", function() {
	getPrediction();

	setInterval(updateTimer, 101);

	pollServerTime();

	document.getElementById("subscribebutton").addEventListener("click", sendSubscription);
	document.getElementById("updatebutton").addEventListener("click", updateServer);
});
