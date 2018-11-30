var schedule_url = window.location.href;
var secretcode = "";
var id = "";
validatePage();

function validatePage(){
	var n = schedule_url.indexOf(".html?");
	if (n < 0){
		alert("Need to have a secret code to review any schedule!");
		window.location.replace("index.html");
	} else {
		var index = n+6;
		secretcode = schedule_url.substring(index, index+10);
		id = schedule_url.substring(index+10);
	}
}

console.log(schedule_url);
function toggleCalendar(arg) {
	var calDiv = document.getElementById("calendarView");
	var weekButt = document.getElementsByClassName("cal-btn");
	var showDiv = document.getElementById("showCal");
	var hideDiv = document.getElementById("hideCal");
	
	if (arg){
		if (document.getElementById("calendarBody").children.length <= 1) {
			showTimeSlots();
		}

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
	// request.open('GET', 'https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/2?week=2011-04-18T00:00:00.00Z', true);
	// request.setRequestHeader('Authorization', 'ywoAcCBGpM');
	console.log('https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/'+id);
	request.open('GET', 'https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/'+id, true);
	request.setRequestHeader('Authorization', secretcode);
	// console.log('OPENED', request.status);
	request.onload = function () {
		// console.log('DONE', request.status);
		// Access JSON data
		var data = JSON.parse(this.response);
		console.log(data);

		// If the response is ok, put the data in the table
		if (request.status >= 200 && request.status < 400) {
			// Get the calendarView <table> element with id="calendar"
			var calenderBody = document.getElementById("calendarBody");

			// The first column will contain the date information
			// Then for each of the days in the week (Mon-Fri), add the TimeSlot's availability to a new cell in the table
			for (colNum = 0; colNum < 6; colNum++) {
				// In the first column, add the time
				if (colNum == 0) {
					// Keep track of the slots that have been used so far
					var slot = 0;
					
					// console.log(data.message);
					
					// Calculate the maximum number of rows, based on the number of TimeSlots per day
					var maxRow = data.timeslots.length / 5;
					
					// For each row in the table, fill in the timeslot data
					for (rowNum = 0; rowNum < maxRow; rowNum++) {
						// Create a new empty row in the table
						var row = calenderBody.insertRow(rowNum);
					
						// Create a new cell <td> element at the current row and column
						var cell = row.insertCell(colNum);

						// Set the cell's contents
						// var n = data.timeslots[slot].start_date.indexOf(":");
						// cell.innerHTML = data.timeslots[slot].start_date.substring(n-2, n+3);
						// var slotTime = new Date(data.timeslots[slot].start_date);
						// cell.innerHTML = data.timeslots[slot].start_date
						// var dateO = data.timeslots[slot].start_date;
						// console.log("Before1: " + dateO);
						// dateE = dateO.replace(":00Z", ".00Z");
						// console.log("after: " + dateE);
						// dateO = dateO + ".Z";
						// console.log("After: " + dateO);
						var slotTime = new Date(data.timeslots[slot].start_date);
						// var slotTime = new Date(dateE);
						
						// console.log("Slot Time:" + dateO);
						if (slotTime.getMinutes() == 0) {
							cell.innerHTML = slotTime.getHours() +":"+ slotTime.getMinutes() +"0";
						} else {
							cell.innerHTML = slotTime.getHours() +":"+ slotTime.getMinutes();
						}
						
						// Increment the current slot counter
						slot++;
					}
					slot = 0;
				} else {					
					// For each row in the table, add the TimeSlots for the current column
					for (rowNum = 0; rowNum < maxRow; rowNum++) {
						// Create a new cell <td> element at the current row and column
						var cell = calendarBody.rows[rowNum].insertCell(colNum);

						// Set the cell's contents
						cell.innerHTML = data.timeslots[slot].start_date;
						
						// If the TimeSlot is available, show this. Otherwise, show "Unavailable"
						if (data.timeslots[slot].available) {
							cell.className = "availableSlot";
						} else {
							cell.className = "unavailableSlot";
						}

						// Increment the current slot counter
						slot++;
					}
				}
			}

			/*
			// Keep track of the slots that have been used so far
			var slot = 0;

			// Calculate the maximum number of rows, from the lenght of time for TimeSlots and the duration of timeslots
			// var maxRow = (endTime - startTime) / (duration / 60);
			var maxRow = 10;

			// For each row in the table, fill in the timeslot data
			for (rowNum = 0; rowNum < maxRow; rowNum++) {
				// Create a new empty row in the table
				var row = calenderBody.insertRow(rowNum);
			
				// The first column will contain the date information
				// Then for each of the days in the week (Mon-Fri), add the TimeSlot's availability to a new cell in the table
				for (colNum = 0; colNum < 6; colNum++) {
					// Create a new cell <td> element at the current row and column
					var cell = row.insertCell(colNum);
					
					// In the first column, add the time
					if (colNum == 0) {
						cell.innerHTML = data.timeslots[slot].start_date;
					} else { // For the other columns, add the availability
						// If the TimeSlot is available, show this. Otherwise, show "Unavailable"
						if (data.timeslots[slot].available) {
							cell.innerHTML = data.timeslots[slot].start_date;
							cell.className = "availableSlot";
						} else {
							cell.innerHTML = data.timeslots[slot].start_date;
							cell.className = "unavailableSlot";
						}
						// Increment the current TimeSlot counter
						slot++;
					}
				}
			} */
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
