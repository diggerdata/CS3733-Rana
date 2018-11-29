
function toggleCalendar(arg) {
	var calDiv = document.getElementById("calendarView");
	var weekButt = document.getElementsByClassName("cal-btn");
	var showDiv = document.getElementById("showCal");
	var hideDiv = document.getElementById("hideCal");
	
	if (arg){

		for (i = 0; i < weekButt.length; i++) {
			weekButt[i].style.display = 'block';
		}
		calDiv.style.display = "block";
		showDiv.style.display = "none";
		hideDiv.style.display = "block";
	} else {
		for (i = 0; i < weekButt.length; i++) {
			weekButt[i].style.display = 'none';
		}
		calDiv.style.display = "none";
		hideDiv.style.display = "none";
		showDiv.style.display = "block";
	}
	return false;
	
}

function showTimeSlots() {
	// Create new request
	var request = new XMLHttpRequest();

	// Make GET request
	request.open('GET', 'https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/1?week=2011-04-18T00:00:00.00Z', true);
	request.onload = function getTimeSlots() {
		// Access JSON data
		var data = JSON.parse(this.response);

		// If the response is ok, put the data in the table
		if (request.status >= 200 && request.status < 400) {
			return data;
		} else {
			// Error handling
		}
	}

	request.send();
}

function previousWeek() {
}

function nextWeek() {
}

function deleteSchedule() {
	var answer = confirm("Are you sure you want to delete this schedule?");
	if (answer) {
		// schedule is deleted and returns back to home page
		window.location.href = "index.html";
		return false;
	} else {
		// nothing
		return true;
	}
}
