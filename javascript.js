const registrationHalfInterval = 30;
const timerUpdateInterval = 101;

var offset = 0;
var prediction;
var registered = false;

function dateUTC(date) {
	return new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
}

function dateString(date, format) {
	if (isNaN(date)) {
		var sss = "---";
		var ss = "--";
		var mm = "--";
		var hh = "--";
		var DD = "--";
		var MM = "--";
		var YYYY = "----";
		var YY = "--";
	} else {
		var sss = String(date.getMilliseconds()).padStart(3, "0");
		var ss = String(date.getSeconds()).padStart(2, "0");
		var mm = String(date.getMinutes()).padStart(2, "0");
		var hh = String(date.getHours()).padStart(2, "0");
		var DD = String(date.getDate()).padStart(2, "0");
		var MM = String(date.getMonth() + 1).padStart(2, "0");
		var YYYY = String(date.getFullYear()).padStart(2, "0");
		var YY = YYYY % 100;
	}

	format = format.replace("sss", sss);
	format = format.replace("ss", ss);
	format = format.replace("mm", mm);
	format = format.replace("hh", hh);
	format = format.replace("DD", DD);
	format = format.replace("MM", MM);
	format = format.replace("YYYY", YYYY);
	format = format.replace("YY", YY);

	return format;
}

function updateTimer() {
	let ctime = new Date();
	let stime = new Date(ctime.getTime() + offset);

	document.getElementById("stime").innerHTML = dateString(stime, "hh:mm:ss.sss");
	document.getElementById("sdate").innerHTML = dateString(stime, "DD.MM.YY");

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
		document.getElementById("prediction").innerHTML = dateString(prediction, "hh:mm:ss.sss");
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
			time = dateUTC(time);

			// predict based on previous measurements
			let delta = i * sxx - sx * sx;
			let a = (i * sxy - sx * sy) / delta;
			let b = (sy * sxx - sx * sxy) / delta;

			let days = Math.floor(msecs / (24 * 60 * 60 * 1000));
			let msecs_pred = a * days + b;
			let time_pred = new Date(msecs_pred);
			time_pred = dateUTC(time_pred);

			let row = table.insertRow(1);
			let cell1 = row.insertCell();
			let cell2 = row.insertCell();
			let cell3 = row.insertCell();
			let cell4 = row.insertCell();
			cell1.innerHTML = dateString(time, "DD.MM.YY");
			cell2.innerHTML = dateString(time, "hh:mm:ss");
			let offset = ((msecs - msecs_pred) / 1000).toFixed(2);
			let sign = offset > 0 ? "+" : "";
			if (!isNaN(offset)) {
				cell3.innerHTML = dateString(time_pred, "hh:mm:ss.sss");
				cell4.innerHTML = sign + offset + " s";
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
