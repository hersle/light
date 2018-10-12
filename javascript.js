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

// let stime = new Date(<?php echo microtime(true) * 1000 ?>);
// let ctime = new Date();
// let offset = stime.getTime() - ctime.getTime();
// let prediction = new Date(<?php echo shell_exec("python3 light.py 2>&1") ?>);
// document.getElementById("prediction").innerHTML = timeString(prediction, true);

function updatePrediction() {
	document.getElementById("prediction").innerHTML = timeString(prediction, true);
}

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
// updateTimer();
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
	xhr.send();
}
//updateServer();
