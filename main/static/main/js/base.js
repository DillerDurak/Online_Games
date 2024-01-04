const menu = document.querySelector('.profile')
const dropDown = document.querySelector('.dropdown-content')


menu.addEventListener('click', ()=>{
    dropDown.classList.toggle('active')
})

window.onclick = function(event) {
    if (!event.target.matches('.profile')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('active')) {
          openDropdown.classList.remove('active');
        }
      }
    }
  }
