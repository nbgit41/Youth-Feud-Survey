let flippedStates = {}; // Store flipped states

//-------------------------------Update stuff-------------------------------------

async function updateAllTheThings(){
    console.log("update all the things")
    const response = await fetch(`/update-all-the-things`, {});
    let data = await response.json();

    //question text
    document.getElementById("question-text").innerText = data.question;
    //scores
    document.getElementById("Boys-Score").innerText = `Boys Score: ${data.boys_score}`;
    document.getElementById("Girls-Score").innerText = `Girls Score: ${data.girls_score}`;
    //strikes
    document.getElementById("strikes").innerText = `Strikes: ${data.strikes}`;

    // Get the answers
    let answers = data.answers;
    let gameBoard = document.querySelector(".game_board");

    // Clear existing tiles
    gameBoard.innerHTML = "";

    // Create new tiles based on the number of answers
    answers.forEach((answer, index) => {
        let tile = document.createElement("pre");
        tile.id = `backend-tile-${index + 1}`;
        tile.dataset.answer = answer.text; // Store answer text

        // Keep the tile flipped if it was previously flipped
        if (flippedStates[index + 1]) {
            tile.innerText = answer.text; // Show answer
            tile.classList.add("flipped");
        } else {
            // tile.innerText = answer.points; // Show points
            tile.innerText = answer.text;
        }

        // Add event listener to toggle flipping
        tile.addEventListener("click", function() {
            let isFlipped = flippedStates[index + 1] || false;
            fetch(`/flip/${index + 1}`, {
                method: "POST",
                body: JSON.stringify({ flip_state: !isFlipped }),
                headers: { "Content-Type": "application/json" }
            })
                .then(() => console.log(`Tile ${index + 1} flipped from backend`))
                .catch(error => console.error("Error flipping tile:", error));
        });

        gameBoard.appendChild(tile);
    });

    // Adjust game board layout dynamically
    adjustGameBoardLayout(answers.length);

    updateAllTheThings();
}

setInterval(updateAllTheThings, 1000);

// Function to dynamically adjust the grid layout based on the number of answers
function adjustGameBoardLayout(answerCount) {
    let gameBoard = document.querySelector(".game_board");

    if (answerCount <= 3) {
        gameBoard.style.gridTemplateColumns = `repeat(${answerCount}, 1fr)`;
        gameBoard.style.gridTemplateRows = "1fr";
    } else if (answerCount <= 6) {
        gameBoard.style.gridTemplateColumns = "repeat(3, 1fr)";
        gameBoard.style.gridTemplateRows = "repeat(2, 1fr)";
    } else {
        gameBoard.style.gridTemplateColumns = "repeat(4, 1fr)";
        gameBoard.style.gridTemplateRows = "repeat(3, 1fr)";
    }
}

async function forceUpdateAllTheThings(){
    updateAllTheThings()
}

//--------------------------------Flip stuff--------------------------------------


// Initialize Socket.IO connection
const socket = io.connect(window.location.origin);

// Listen for flip updates from backend
socket.on("flip_update", (data) => {
    console.log(`Backend received flip event for tile ${data.tile}: ${data.flipped}`);

    let tile = document.getElementById(`backend-tile-${data.tile}`);
    if (tile) {
        flippedStates[data.tile] = data.flipped; // Save flipped state
        tile.innerText = data.flipped ? tile.dataset.answer : "OOPS";
        tile.classList.toggle("flipped", data.flipped);
    }
});

// Listen for reset flips from backend when a new question is loaded
socket.on("reset_flips", () => {
    console.log("Resetting all flipped tiles for new question.");
    flippedStates = {}; // Clear flipped states

    // Reset all tile styles on screen
    document.querySelectorAll(".game_board pre").forEach(tile => {
        tile.innerText = "Loading"; // Reset to point value
        tile.classList.remove("flipped"); // Remove flipped class
    });
});

//-------------------------------Question add or sub------------------------------

function nextQuestionPlzBro() {
    fetch(`/next-question-plz-bro`, {})
        .then(() => console.log('next question plz'))
        .catch(error => console.error('Error:', error));
}

function waitNoGoBack() {
    fetch(`/wait-no-go-back-bro`, {})
        .then(() => console.log('next question plz'))
        .catch(error => console.error('Error:', error));
}

//-------------------------------Buzzer-------------------------------------------

async function updateBuzzerStatus() {
    const response = await fetch("/status"); // Fetch buzzer status from server
    const data = await response.json();

    const playerThatBuzzedDiv = document.getElementById("player_that_buzzed");
    if (data.player) {
        playerThatBuzzedDiv.innerText = `${data.player} has buzzed`;
    } else {
        playerThatBuzzedDiv.innerText = "no buzz yet";
    }
}