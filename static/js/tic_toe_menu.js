//TIC TOC TOE MENU

const avatar = document.getElementById('avatar');
const avatarBtn = document.getElementById('avatar-btn');
const url = 'https://avatars.dicebear.com/api/miniavs/';
let avatarURL = '';

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min; //Максимум и минимум включаются
  }

function getRandomStr(length){
    // Declare all characters
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // Pick characers randomly
    let str = '';
    for (let i = 0; i < length; i++) {
        str += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return str;
};

avatarBtn.addEventListener('click', ()=>{
    let randomInt = getRandomInt(1,20);
    let string = getRandomStr(randomInt) + '.svg';
    let url2 = url + string;
    avatar.src = url2;
})


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


document.querySelector('.main-form').addEventListener('submit', ()=>{
    image = document.getElementById('avatar').src
    nickname = document.getElementById('nick').value
    data = JSON.stringify({
        'image': image,
        'nickname': nickname
    })
    fetch("http://127.0.0.1:8000/api/v1/game/add-image/", {
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