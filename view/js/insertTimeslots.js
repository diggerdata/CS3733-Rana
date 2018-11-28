/*
Function insertTimeslots() accepts:
 - ID of a <table> element tableID
 - numer of rows in the table rowNum
 - Timeslots for the Schedule timeslots
*/
function insertTimeslots(tableID, rowNum, timeslots) {
    // Find a <table> element with an id tableID:
    var table = document.getElementById(tableID);

    // For each row in the table, add the necessary columns of Timeslots:
    for(r = 0; r < rowNum; r++) {
        // Create an empty <tr> element and add it to the rth position of the table:
        var row = table.insertRow(r);

        // For each column in the row, add the necessary Timeslot cells:
        for(n = 0; n < 5; n++) {
            // Create a cell variable at the correct row and column:
            var cell = row.insertCell(n);
            // Insert the content into a new cell (<td> element):
            cell.innerHTML = timeslots;
        }
    }
}