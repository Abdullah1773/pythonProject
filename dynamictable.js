let mob = [];
let list = [];
let listB = [];
let list1 = ['System Engineering Activities'];

function fetchData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

let isButtonClicked = false; // Add this variable

function handleButtonClick() {
    if (!isButtonClicked) {
        isButtonClicked = true;
        const url = 'http://localhost:5006/JSON_data';
        fetchData(url)
            .then(jsonData => {
                console.log(jsonData);
                mob = jsonData;
                jsonData.forEach(Val => {
                    list.push(Val["Activity"]);
                    listB.push(Val["Artifacts"]);
                });
                CreateTable();
            });
    }
}

// Add event listener to the button
const fetchButton = document.getElementById('fetchButton');
fetchButton.addEventListener('click', handleButtonClick);

function CreateTable() {
    // handleButtonClick()
    let row = list.length + 1; // Set your desired number of rows
    let col = list.length + 1; // Set your desired number of columns
    console.log(row);
    console.log(col);
    var html = "<table id='dataTable' border='1'>";
    for (let r = 0; r < row; r++) {
        html += "<tr>";
        for (let c = 0; c < col; c++) {
            if (r === 0 && c === 0) {
                html += '<td style="background-color: #bdd7ee; font-weight: bold;">System Engineering Activities</td>'; // Empty cell for the top-left corner
            } else if (r === 0) {
                // Display list elements across the first row
                html += `<td >${list[c - 1]}</tdstyle="background-color: #c6e0b4;>`;
            } else if (c === 0) {
                // Display list elements across the first column
                html += `<td >${list[r - 1]}<br></br><button onclick="retrieveData(${r})">View Details</button></td>`;
                // html += `<td>${list[r - 1]}<br></br><button onclick="retrieveData(${r})">View Details</button><button onclick="deleteRow(${r})">Delete</button> </td>`;
            } else if (r === c) {
                // Display listB elements across the diagonal
                let activity = list[r - 1];
                let totalMethods = getTotalMethods(activity);
                if (totalMethods > 0) {
                    html += `<td>${listB[r - 1]} <br>(${totalMethods} Methods) </td>`;
                } else {
                    html += `<td>${listB[r - 1]}</td>`;
                }
            } else if (r > c) {
                // Display listB elements below the diagonal
                html += `<td>${listB[c - 1]}</td>`;
            } else {
                html += '<td></td>'; // Empty cells in the remaining table
            }
        }
        html += "</tr>";
    }
    html += "</table>";
    const dialogContent = `
        <div class="popup"> 
            <button id="closeButton" onclick="closeDetailDialog()">Close</button>
            <div class="overlay"></div> 
            <div class="content">
                <h4>Title </h4> 
                <textarea id="title" rows="4" cols="50"></textarea> 
                <div>
                    <h4>Activity Number</h4>
                    <!-- <input type="text" id="activityNumber" value="Non-editable text" readonly>--> 
                    <textarea id="activityNumber" rows="4" cols="50" readonly ></textarea>
                </div> 
                <div>
                    <h4>Explanation</h4> 
                    <textarea id="explanation" rows="4" cols="50"></textarea>
                </div>
                <div>
                    <h4>Output Artifacts</h4> 
                    <!-- <input type="text" id="outputArtifacts" value="Non-editable text" readonly>--> 
                    <textarea id="outputArtifacts" rows="4" cols="50" ></textarea>
                </div> 
                <div>
                    <h4>Input Artifacts</h4> 
                    <textarea id="inputArtifacts" rows="4" cols="50" readonly></textarea> 
                </div> 
                <h4>Method 1</h4>
                <textarea id="method1" rows="4" cols="50"></textarea>
                <h4>Method 2</h4>
                <textarea id="method2" rows="4" cols="50"></textarea> 
                <h4>Method 3</h4>
                <textarea id="method3" rows="4" cols="50"></textarea>
                <button onclick="saveData()">Save</button>
            </div>
        </div> 
    `;
    html += dialogContent;
    document.getElementById('tablearea').innerHTML = html;
}

function exchangeSelected() {
    let checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    let selectedIds = Array.from(checkboxes).map(checkbox => checkbox.id);
    // Fisher-Yates shuffle
    for (let i = selectedIds.length - 1; i > 0; i--) { /*Problem is due to the three lines, i think*/
        const j = Math.floor(Math.random() * (i + 1));
        [selectedIds[i], selectedIds[j]] = [selectedIds[j], selectedIds[i]];
    }
    // Create a copy of the original list
    let originalList = list.slice();
    // Update the original list with the shuffled values
    selectedIds.forEach((id, index) => {
        const originalIndex = list.indexOf(id);
        list[originalIndex] = originalList[index];
    });
    // Recreate the table
    CreateTable();
}

// Function to retrieve data from the database in JSON format
function retrieveData(row) {
    let id = row - 1;
    document.getElementsByClassName("popup")[0].style.display = "contents";
    document.getElementById("dataTable").style.display = "none";
    document.getElementById("title").value = mob[id].Activity;
    document.getElementById("activityNumber").value = mob[id].id;
    document.getElementById("explanation").value = mob[id].Explanation;
    document.getElementById("method1").value = mob[id].Method1;
    document.getElementById("method2").value = mob[id].Method2;
    document.getElementById("method3").value = mob[id].Method3;
    // Clear previous data from other fields
    document.getElementById("outputArtifacts").value = mob[id].Artifacts;
    document.getElementById("inputArtifacts").value = (id > 0) ? mob[id - 1].Artifacts : '';
}



function closeDetailDialog() {
    document.getElementsByClassName("popup")[0].style.display = "none";
    document.getElementById("dataTable").style.display = "block";
}

function saveData() {
    let id = document.getElementById("activityNumber").value;
    let url = 'http://localhost:5006/' + id + '/edit'; // Get the values of the input fields and trim whitespace
    let editedData = {
        Activity: document.getElementById("title").value.trim(),
        Explanation: document.getElementById("explanation").value.trim(),
        Artifacts: document.getElementById("outputArtifacts").value.trim(),
        Method1: document.getElementById("method1").value.trim(),
        Method2: document.getElementById("method2").value.trim(),
        Method3: document.getElementById("method3").value.trim(),
    };
    console.log('Edited data before removing empty fields:', editedData);
    // Remove empty fields from the editedData object
    Object.keys(editedData).forEach(key => {
        if (editedData[key] === '') {
            console.log(`Deleting empty field ${key}`);
            delete editedData[key];
        }
    });
    console.log('Edited data after removing empty fields:', editedData);
    // Send the edited data to the server
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedData)
    })
    .then(response => {
        if (response.ok) {
            console.log('Data saved successfully');
            // Refresh the page after saving data
            location.reload();
        } else {
            console.error('Failed to save data:', response.statusText);
        }
    })
    .catch(error => console.error('Error saving data:', error));
}

function refreshPage() {
    location.reload();
}

// Function to handle the response after adding or deleting rows
function handleResponse(response) {
    if (response.ok) {
        console.log('Operation successful');
        // Refresh the table content without reloading the page
        // handleButtonClick();
        refreshPage();
    } else {
        console.error('Operation failed:', response.statusText);
    }
}

// Function to add a new row
function addToArray() {
    let newData = {
        Activity: '',
        Explanation: '',
        Artifacts: '',
        Methods: ''
    };
    fetch('http://localhost:5006/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newData)
    })
    .then(response => handleResponse(response))
    .catch(error => console.error('Error adding new element:', error));
}

function getTotalMethods(activity) {
    // Iterate through the 'mob' array to count the total number of methods for the given activity
    let totalMethods = 0;
    for (let i = 0; i < mob.length; i++) {
        if (mob[i].Activity === activity) {
            if (mob[i].Method1.trim() !== '') totalMethods++;
            if (mob[i].Method2.trim() !== '') totalMethods++;
            if (mob[i].Method3.trim() !== '') totalMethods++;
        }
    }
    return totalMethods;
}