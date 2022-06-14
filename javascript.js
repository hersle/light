const registrationHalfInterval = 30;
const timerUpdateInterval = 101;

var offset = 0;
var prediction;
var registered = false;

// Returns the given date represented with a UTC timezone
function dateUTC(date) {
	return new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
}

function dateUTCLocal(date) {
	return new Date(date.getTime() - date.getTimezoneOffset() * 60 * 1000);
}

function stripDateTimeUTC(date) {
	date.setUTCHours(0);
	date.setUTCMinutes(0);
	date.setUTCSeconds(0);
	date.setUTCMilliseconds(0);
	return date;
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

	let msecs = Math.abs(stime - prediction);
	let h = Math.floor(msecs / 3600000);
	let m = Math.floor((msecs % 3600000) / 60000);
	let s = Math.floor((msecs % 60000) / 1000);
	let ms = msecs % 1000;
	let diff = new Date(0, 0, 0, h, m, s, ms);

	let sign = stime < prediction ? "−" : "+";
	let text = sign + dateString(diff, "hh:mm:ss.sss");
	let color = "";
	if (registered || Math.abs(msecs / 1000) > registrationHalfInterval) {
		color = "grey";
	} else {
		color = "green";
	}
	document.getElementById("updatebuttonsubtext").innerHTML = text;
	document.getElementById("updatebutton").style.backgroundColor = color;
}

function updateServerTime() {
	let req = new XMLHttpRequest();
	req.open("GET", "time.php");
	req.addEventListener("load", function() {
		let ms = parseInt(req.response);
		let stime = new Date(ms);
		let ctime = new Date();
		offset = stime.getTime() - ctime.getTime();
	});
	req.send();
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
		let success = req.response === "Slukking registrert.";
		let color = "";
		if (success) {
			color = "green";
		} else {
			color = "red";
		}
		document.getElementById("registerresponse").innerHTML = req.response;
		document.getElementById("registerresponse").style.display = "block";
		document.getElementById("registerresponse").style.color = color;
		document.getElementById("registerresponse").style.borderColor = color;
		if (success) {
			updateTable();
			updateStatus();
			updatePrediction();
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
		document.getElementById("subscriberesponse").innerHTML = req.response;
		document.getElementById("subscriberesponse").style.display = "block";
		document.getElementById("emailinput").value = "";
		//window.location.hash = "subscriberesponse"
	});
	req.send("email=" + email);
}

function updateTable() {
	let req = new XMLHttpRequest();
	req.open("GET", "list.php");
	req.addEventListener("load", function() {
		let tabletop = document.getElementById("lighttabletop");
		let tablebottom = document.getElementById("lighttablebottom");

		let sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0;

		let meas_pred_list = req.response.split("\n");
		let n = meas_pred_list.length - 1;
		for (let i = 0; i < n; i++) { // skip last empty line
			let meas_pred = meas_pred_list[i].split(" ");
			let meas = dateUTC(new Date(parseInt(meas_pred[0])));
			let pred = new Date(parseInt(meas_pred[1]));

			if (n - i <= 5) {
				var row = tabletop.insertRow(1);
			} else {
				var row = tablebottom.insertRow(0);
			}

			let cell1 = row.insertCell();
			let cell2 = row.insertCell();
			let cell3 = row.insertCell();
			let cell4 = row.insertCell();
			cell1.innerHTML = dateString(meas, "DD.MM.YY");
			cell2.innerHTML = dateString(meas, "hh:mm:ss");
			let offset = ((meas - pred) / 1000);
			let sign = offset > 0 ? "+" : "−";
			offset = Math.abs(offset);
			if (!isNaN(offset)) {
				offset = offset.toFixed(1);
				cell3.innerHTML = dateString(pred, "hh:mm:ss.sss");
				cell4.innerHTML = sign + offset + " s";
				if (offset >= 20) {
					cell4.style.backgroundColor = "red";
				} else if (offset >= 10) {
					cell4.style.backgroundColor = "orange";
				} else if (offset >= 5) {
					cell4.style.backgroundColor = "yellow";
				}
			}
		}

		// determine streak by counting backwards
		let currdate = dateUTCLocal(new Date());
		let streak = 0;
		for (let i = n - 1; i >= 0; i--) {
			let msecs = parseInt(meas_pred_list[i].split(" ")[0]);
			let prevdate = new Date(msecs);

			let currdatedate = stripDateTimeUTC(currdate);
			let prevdatedate = stripDateTimeUTC(prevdate);
			let diff = currdatedate.getTime() - prevdatedate.getTime();
			if (diff <= 24 * 60 * 60 * 1000) {
				streak++;
			} else {
				break;
			}

			currdate = prevdate;
		}
		let text = "";
		if (streak == 1) {
			text = streak + " dag";
		} else {
			text = streak + " dager";
		}
		document.getElementById("streakcount").innerHTML = text;
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
	document.getElementById("tablecollapser").addEventListener("click", function(){
		if (document.getElementById("lighttablebottom").style.display == "none") {
			document.getElementById("lighttablebottom").style.display = "";
			document.getElementById("tablecollapser").innerHTML = "Vis færre målinger"
		} else {
			document.getElementById("lighttablebottom").style.display = "none";
			document.getElementById("tablecollapser").innerHTML = "Vis alle målinger"
		}
	});

	document.getElementById("tablecollapser").click();
});
