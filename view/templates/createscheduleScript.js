var post_url = "https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/"
function validateScheduleCreation() {
	// this is so ugly - needs refactoring
	
	var schedulename = document.getElementById("scheduleName").value;
	var s_date = document.getElementById("startDate").value;
	var e_date = document.getElementById("endDate").value;
	var s_time = document.getElementById("startTime").value;
	var s_time_type = document.getElementById("stType").value;
	var e_time = document.getElementById("endTime").value;
	var e_time_type = document.getElementById("etType").value;
	var slotduration = document.getElementById("slotDuration").value;
	var username = document.getElementById("userName").value;
	var email = document.getElementById("userEmail").value;
	
	// changes time to 24 hr time
	if (s_time_type == "PM" && s_time < 12) {
		s_time = parseInt(s_time) + 12;
	} else if (e_time_type == "PM" && e_time < 12) {
		e_time = parseInt(e_time) + 12;
	}
	
	// date and time check
	if (e_date < s_date) {
		alert("End date can't be less than start date!");
		return false;
	} else if (e_date == s_date && e_time <= s_time) {
		alert("Start time cannot be greater than or equal to the end time!");
		return false;
	}
	
	// creates javascript date format
	if (s_time < 10) {
		s_time = "0"+s_time;
	} else if (e_time < 10) {
		e_time = "0"+e_time;
	}
	
	var startDate = s_date+"T"+s_time+":00:00.00Z";
	var endDate = e_date+"T"+e_time+":00:00.00Z";
	
	var formData = new FormData();
	formData.append('name', schedulename);
	formData.append('start_date', startDate);
	formData.append('end_date', endDate);
	formData.append('duration', parseInt(slotduration));
	formData.append('username', username);
	formData.append('email', email);
	
	for (var value of formData.entries()) {
	   console.log(value); 
	}
	
	var object = {};
	for (const [key, value]  of formData.entries()) {
		object[key] = value;
		if (key == "duration") {
			object[key] = parseInt(value);
		}
	}
	
	var request = new XMLHttpRequest();
	request.open("POST", post_url, true);
	request.send(object);
	request.onloadend = function(){
		if(request.readyState == XMLHttpRequest.DONE){
			console.log(request.responseText);
			alert("Calendar Created");
		}else{
			alert("Failed!");
		}
		
	};
	
	alert("ah");
	
	// var request = new XMLHttpRequest();
	// request.open('POST', 'https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/', true);
	
	// var responseObject = {};
	// postData(`http://example.com/answer`, object)
		// .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
		// .catch(error => console.error(error));
	
	// fetch(`https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/`, object).then(function(response){
		// console.log(response.json());
	// });
	
	// postData(`https://sqc1z962y5.execute-api.us-east-2.amazonaws.com/dev/schedule/`, object)
	// .then(data => console.log("me")) // JSON-string from `response.json()` call
	// .catch(error => console.error(error));
	
	// console.log(JSON.stringify(responseObject));
	// alert("complete\n");
	
	// send information to API and create schedule
	// once created, then approve submission
}

// function postData(url = ``, data = {}) {
  // // Default options are marked with *
    // return fetch(url, {
        // method: "POST", // *GET, POST, PUT, DELETE, etc.
        // mode: "cors", // no-cors, cors, *same-origin
        // // cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        // // credentials: "same-origin", // include, *same-origin, omit
        // // headers: {
            // // "Content-Type": "application/json; charset=utf-8",
            // "Content-Type": "application/x-www-form-urlencoded",
        // // },
        // // redirect: "follow", // manual, *follow, error
        // // referrer: "no-referrer", // no-referrer, *client
        // body: JSON.stringify(data), // body data type must match "Content-Type" header JSON.stringify(data)
    // })
    // .then(response => response.json()); // parses response to JSON
// }
