const registrationHalfInterval = 60000;
const timerUpdateInterval = 101;

var offset = 0;
var prediction;

function timeString(date) {
	let h = String(date.getHours()).padStart(2, "0");
	let m = String(date.getMinutes()).padStart(2, "0");
	let s = String(date.getSeconds()).padStart(2, "0");
	let ms = String(date.getMilliseconds()).padStart(3, "0");
	return h + ":" + m + ":" + s + "." + ms;
}

function dateString(date) {
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

	if (document.getElementById("updatebutton").style.backgroundColor == "grey") {
	} else if (Math.abs(stime - prediction) <= registrationHalfInterval) {
		document.getElementById("updatebutton").style.backgroundColor = "green";
	} else {
		document.getElementById("updatebutton").style.backgroundColor = "red";
		document.getElementById("updatebutton").innerHTML = "Lysregistrering åpner om " + Math.floor(((prediction - registrationHalfInterval) - stime) / 1000) + " sekunder";
	}
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
	req.open("GET", "prediction.php");
	req.addEventListener("load", function() {
		let secs = parseInt(req.response);
		prediction = new Date(secs);
		document.getElementById("prediction").innerHTML = timeString(prediction);
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

window.addEventListener("load", function() {
	updatePrediction();
	updateServerTime();
	setInterval(updateTimer, timerUpdateInterval);

	document.getElementById("subscribebutton").addEventListener("click", subscribe);
	document.getElementById("updatebutton").addEventListener("click", register);

});
