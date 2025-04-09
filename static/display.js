let flippedStates = {}; // Store flipped states

async function updateAllTheThings(){
    console.log("update all the things")
    const response = await fetch(`/update-all-the-things`, {});

    let data = await response.json();
    //question text
    document.getElementById("question-text").innerText = data.question;
    //scores
    document.getElementById("Boys-Score").innerText = data.boys_score;
    document.getElementById("Girls-Score").innerText = data.girls_score;
    //strikes

    document.querySelector(".strikes h3").innerText = `Strikes: ${data.strikes}`;
    // Get the answers
    let answers = data.answers;
    let gameBoard = document.querySelector(".game_board");

    // Clear existing tiles
    gameBoard.innerHTML = "";

    // Create new tiles based on the number of answers
    answers.forEach((answer, index) => {
        let tile = document.createElement("pre");
        tile.id = index + 1;
        tile.dataset.answer = answer.text; // Store answer text

        // Keep the tile flipped if it was previously flipped
        if (flippedStates[index + 1]) {
            tile.innerText = answer.text; // Show answer
            tile.classList.add("flipped");
        } else {
            tile.innerText = answer.points; // Show points
        }

        gameBoard.appendChild(tile);
    });


    updateBuzzerStatus();
    // Adjust game board layout dynamically
    adjustGameBoardLayout(answers.length);

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

//--------------------------------Buzzer------------------------------------------
async function updateBuzzerStatus() {
    const response = await fetch("/status"); // Fetch buzzer status from server

    const data = await response.json();
    const playerThatBuzzedDiv = document.querySelector(".player_that_buzzed");
    if (data.player) {
        playerThatBuzzedDiv.innerText = `${data.player} has buzzed`;
    } else {
        playerThatBuzzedDiv.innerText = "";
    }


}

//--------------------------------Flip stuff--------------------------------------

// Initialize Socket.IO connection
const socket = io.connect(window.location.origin);

// Listen for flip updates from backend
socket.on("flip_update", (data) => {
    console.log(`Tile ${data.tile} flipped state: ${data.flipped}`);

    let tile = document.getElementById(data.tile);
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