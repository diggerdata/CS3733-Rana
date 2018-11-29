
function toggleCalendar(arg) {
	var calDiv = document.getElementById("calendarView");
	var weekButt = document.getElementsByClassName("cal-btn");
	var showDiv = document.getElementById("showCal");
	var hideDiv = document.getElementById("hideCal");
	
	if (arg){
		var timeSlotsData = showTimeSlots();

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
	request.onload = function () {
		// Access JSON data
		var data = JSON.parse(this.response);

		// If the response is ok, put the data in the table
		if (request.status >= 200 && request.status < 400) {
			console.log(data.name);
			
			// Get the calendarView <table> element with id="calendar"
			var calenderTable = document.getElementById("calendarBody");

			// Keep track of the slots that have been used so far
			var slot = 0;

			// Calculate the maximum number of rows, from the lenght of time for TimeSlots and the duration of timeslots
			// var maxRow = (endTime - startTime) / (duration / 60);
			var maxRow = 10;

			// For each row in the table, fill in the timeslot data
			for (rowNum = 0; rowNum < maxRow; rowNum++) {
				// Create a new empty row in the table
				var row = calenderTable.insertRow(rowNum);

				// For each of the days in the week (Mon-Fri), add the TimeSlot's availability to a new cell in the table
				for(day = 0; day < 5; day++) {
					var cell = row.insertCell(day);
					if (data.timeslots[slot].available) {
						cell.innerHTML = "Available";
					} else {
						cell.innerHTML = "Unavailable";
					}
					slot++;
				}
			}
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
