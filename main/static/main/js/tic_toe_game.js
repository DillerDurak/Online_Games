//TIC TOC TOE GAME
var roomCode = document.getElementById("game_board").getAttribute("room_code");
var char_choice = document.getElementById("game_board").getAttribute("char_choice");
var nickname = document.getElementById("game_board").getAttribute("nickname");
var user1 = document.querySelector('#user1');
var user2 = document.querySelector('#user2');
var img1 = document.querySelector('#p1_img');
var img2 = document.querySelector('#p2_img');
var nick_1 = document.querySelector('#p1_nick');
var nick_2 = document.querySelector('#p2_nick');


var connectionString = 'ws://' + window.location.host + '/ws/tic-tac/play/' + roomCode + '/';
const gameSocket = new WebSocket(connectionString);
// Game board for maintaing the state of the game

connect();



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');

fetch('http://' + window.location.host + '/api/v1/game/add-user/', {
    method: 'POST',
    body: JSON.stringify({
        'room_code': roomCode,
    }),
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }
})
.then(response => response.json())
.then(data => {
    console.log(data)
    img1.src = data['player_1']
    img2.src = data['player_2']
    console.log(data['player_1'], data['player_2'])
})
.catch(error => console.log('error: ', error))

function addRating(nickname){
    data = JSON.stringify({
        'username': nickname
    })
    let url = 'http://' + window.location.host + '/api/v1/user/change-rating/';
    fetch(url, {
        method: 'POST',
        body: data,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('error: ', error))
}

var gameBoard = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
];
// Winning indexes.
winIndices = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
let moveCount = 0; //Number of moves done
let myturn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArray = document.getElementsByClassName('square');
for (var i = 0; i < elementArray.length; i++){
    elementArray[i].addEventListener("click", event=>{
        const index = event.composedPath()[0].getAttribute('data-index');
        if(gameBoard[index] == -1){
            if(!myturn){
                alert("Wait for other to place the move")
            }
            else{
                myturn = false;
                document.getElementById("alert_move").style.display = 'none'; // Hide
                make_move(index, char_choice, nickname);
            }
        }
    })
}

// Make a move
function make_move(index, player, nickname){
    index = parseInt(index);
    let data = {
        "event": "MOVE",
        "message": {
            "index": index,
            "player": player,
            "nickname": nickname
        },
    }

    if(gameBoard[index] == -1){
        // if the valid move, update the gameboard
        // state and send the move to the server.
        moveCount++;
        if(player == 'X')
            gameBoard[index] = 1;
        else if(player == 'O')
            gameBoard[index] = 0;
        else{
            alert("Invalid character choice");
            return false;
        }
        gameSocket.send(JSON.stringify(data))
    }
    // place the move in the game box.
    elementArray[index].innerHTML = player;
    // check for the winner
    const win = checkWinner();
    if(myturn){
        // if player winner, send the END event.
        if(win){
            image = '';
            if (nickname === nick_1.textContent){
                image = img1.src
            }
            else if (nickname === nick_2.textContent){
                image = img2.src
            }
            data = {
                "event": "END",
                "message": `${nickname} is a winner. Play again?`,
                'winner': nickname,
                'image': image
            }
            addRating(nickname)
            

            gameSocket.send(JSON.stringify(data))
            
        }
        else if(!win && moveCount == 9){
            data = {
                "event": "END",
                "message": "It's a draw. Play again?"
            }
            gameSocket.send(JSON.stringify(data))
        }
    }
}

// function to reset the game.
function reset(){
    gameBoard = [
        -1, -1, -1,
        -1, -1, -1,
        -1, -1, -1,
    ];
    moveCount = 0;
    myturn = true;
    document.getElementById("alert_move").style.display = 'inline';
    for (var i = 0; i < elementArray.length; i++){
        elementArray[i].innerHTML = "";
    }
}

// check if their is winning move
const check = (winIndex) => {
    if (
      gameBoard[winIndex[0]] !== -1 &&
      gameBoard[winIndex[0]] === gameBoard[winIndex[1]] &&
      gameBoard[winIndex[0]] === gameBoard[winIndex[2]]
    )   return true;
    return false;
};

// function to check if player is winner.
function checkWinner(){
    let win = false;
    if (moveCount >= 5) {
      winIndices.forEach((w) => {
        if (check(w)) {
          win = true;
          windex = w;
        }
      });
    }
    return win;
}

// Main function which handles the connection
// of websocket.
function connect() {
    gameSocket.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        gameSocket.send(JSON.stringify({
            "event": "START",
            "message": nickname
        }));
    };

    gameSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    // Sending the info about the room
    gameSocket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        data = data["payload"];
        let message = data['message'];
        let event = data["event"];
        let winner = data['winner'];
        let image = data['image'];
        switch (event) {
            case "START":
                reset();
                alert('started')
                break;
            case "END":
                // alert(message);
                document.querySelector('#winner').textContent = `Winner is ${winner}`
                document.querySelector('#winner-avatar').src = image

                if (winner === nick_1.textContent){
                    document.querySelector('.popup__body').style.backgroundColor = 'rgb(134, 134, 206)'
                }
                else{
                    document.querySelector('.popup__body').style.backgroundColor = 'rgb(202, 120, 114)'
                }

                document.querySelector('#popup').classList.add('active')

                setTimeout(()=>{
                    document.querySelector('#popup').classList.remove('active')
                }, 3000);

                reset();
                break;
            case "MOVE":
                if(message["player"] != char_choice){
                    make_move(message["index"], message["player"], message['nickname'])
                    myturn = true;
                    document.getElementById("alert_move").style.display = 'inline';
                }
                console.log('Moved')
                break;
            default:
                console.log("No event")
        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}

window.addEventListener('beforeunload', ()=>{

    data = JSON.stringify({
        'nickname': document.querySelector('#user_username').textContent
    })
    fetch('http://'+window.location.host + '/api/v1/game/delete-user/', {
        method: 'POST',
        body: data,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('error: ', error))
    

})
//call the connect function at the start.
