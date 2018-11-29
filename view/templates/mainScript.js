function validateCode() {
	var x = document.forms["reviewForm"]["secretCode"].value;
	if (x != "123abc") {
		alert("Incorrect Secret Code!");
		return false;
	}
}

// if (x == "org123") {
		// window.location.href = "review_schedule.html";
	// } else if (x == "part123"){
		// window.location.href = "review_meeting.html";
	// } else {
		// alert("Incorrect Secret Code!");
		// return false;
	// }
