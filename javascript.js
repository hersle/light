const registrationHalfInterval = 30;
const timerUpdateInterval = 101;

var offset = 0;
var prediction;
var registered = false;

function timeString(date) {
	if (isNaN(date)) {
		return "--:--:--.---";
	}
	let h = String(date.getHours()).padStart(2, "0");
	let m = String(date.getMinutes()).padStart(2, "0");
	let s = String(date.getSeconds()).padStart(2, "0");
	let ms = String(date.getMilliseconds()).padStart(3, "0");
	return h + ":" + m + ":" + s + "." + ms;
}

function dateString(date) {
	if (isNaN(date)) {
		return "--:--:--.---";
	}
	let d = String(date.getDate()).padStart(2, "0");
	let m = String(date.getMonth() + 1).padStart(2, "0");
	let y = String(date.getFullYear()).padStart(2, "0");
	return d + "." + m + "." + y;
}

function updateTimer() {
	let ctime = new Date();
	let stime = new Date(ctime.getTime() + offset);

	document.getElementById("stime").innerHTML = timeString(stime);
	document.getElementById("sdate").innerHTML = dateString(stime);

	let text = "";
	let color = "";
	let secs = Math.floor((stime - prediction) / 1000);
	if (registered) {
		text = "Slukking registrert";
		color = "grey";
	} else if (secs < -registrationHalfInterval) {
		secs = -(secs + registrationHalfInterval);
		text = "Registrering åpner om ";
		if (secs <= 60) {
			text += secs + " sekunder";
		} else if (secs <= 60 * 60) {
			let min = Math.floor(secs / 60);
			text += min + " minutter";
		} else {
			let hours = Math.floor(secs / (60 * 60));
			text += hours + " timer";
		}
		color = "grey";
	} else if (secs > +registrationHalfInterval) {
		text = "Slukking stengt";
		color = "grey";
	} else {
		text = "Registrér slukking";
		color = "green";
	}
	document.getElementById("updatebutton").innerHTML = text;
	document.getElementById("updatebutton").style.backgroundColor = color;

	/*
	if (document.getElementById("updatebutton").style.backgroundColor == "grey") {
	} else if (Math.abs(stime - prediction) <= registrationHalfInterval) {
		document.getElementById("updatebutton").style.backgroundColor = "green";
	} else {
		document.getElementById("updatebutton").style.backgroundColor = "red";
		document.getElementById("updatebutton").innerHTML = "Lysregistrering åpner om " + Math.floor(((prediction - registrationHalfInterval) - stime) / 1000) + " sekunder";
	}
	*/
}

function updateServerTime() {
	let req = new XMLHttpRequest();
	req.open("GET", "time.php");
	req.addEventListener("load", function() {
		let secs = parseInt(req.response);
		let stime = new Date(secs);
		let ctime = new Date();
		offset = stime.getTime() - ctime.getTime();
	});
}

function updatePrediction() {
	let req = new XMLHttpRequest();
	req.open("GET", "predict.php");
	req.addEventListener("load", function() {
		let secs = parseInt(req.response);
		prediction = new Date(secs);
		document.getElementById("prediction").innerHTML = timeString(prediction);
	});
	req.send();
}

function updateStatus() {
	let req = new XMLHttpRequest();
	req.open("GET", "status.php");
	req.addEventListener("load", function() {
		if (req.response === "yes") {
			registered = false;
		} else {
			registered = true;
		}
	});
	req.send();
}

function register() {
	var req = new XMLHttpRequest();
	req.open("POST", "post.php");
	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.addEventListener("load", function() {
		if (req.readyState == 4 && req.response === "Registrert.") {
			location.reload();
		} else {
			document.getElementById("response").innerHTML = req.response;
			document.getElementById("response").style.display = "block";
		}
	});
	req.send();
}

function subscribe() {
	let req = new XMLHttpRequest();
	let email = document.getElementById("emailinput").value;

	req.open("POST", "subscribe.php");
	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.addEventListener("load", function() {
		document.getElementById("response").innerHTML = req.response;
		document.getElementById("response").style.display = "block";
		document.getElementById("emailinput").value = "";
	});
	req.send("email=" + email);
}

function updateTable() {
	let req = new XMLHttpRequest();
	req.open("GET", "list.php");
	req.addEventListener("load", function() {
		let table = document.getElementById("lighttable");

		let sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0;

		let times = req.response.split("\n");
		let n = times.length - 1;
		for (let i = 0; i < n; i++) { // skip last empty line
			let msecs = parseInt(times[i]);
			let time = new Date(msecs);

			// predict based on previous measurements
			let delta = i * sxx - sx * sx;
			let a = (i * sxy - sx * sy) / delta;
			let b = (sy * sxx - sx * sxy) / delta;

			let days = Math.floor(msecs / (24 * 60 * 60 * 1000));
			let msecs_pred = a * days + b;
			let time_pred = new Date(msecs_pred);

			let row = table.insertRow(1);
			let cell1 = row.insertCell();
			let cell2 = row.insertCell();
			let cell3 = row.insertCell();
			let cell4 = row.insertCell();
			let cell5 = row.insertCell();
			cell1.innerHTML = dateString(time);
			cell2.innerHTML = timeString(time);
			cell3.innerHTML = timeString(time_pred);
			let offset = ((msecs - msecs_pred) / 1000).toFixed(2);
			let sign = offset > 0 ? "+" : "";
			if (!isNaN(offset)) {
				cell4.innerHTML = sign + offset + " s";
				if (offset > 5) {
					cell4.style.backgroundColor = "red";
					cell5.innerHTML = "Ja";
				} else {
					cell4.style.backgroundColor = "green";
					cell5.innerHTML = "Nei";
				}
			}

			// for next
			sx += days;
			sy += msecs;
			sxx += days * days;
			sxy += days * msecs;
			syy += msecs * msecs;
		}
	});
	req.send();
}

window.addEventListener("load", function() {
	updatePrediction();
	updateServerTime();
	updateStatus();
	updateTable();
	setInterval(updateTimer, timerUpdateInterval);

	document.getElementById("subscribebutton").addEventListener("click", subscribe);
	document.getElementById("updatebutton").addEventListener("click", register);
});
