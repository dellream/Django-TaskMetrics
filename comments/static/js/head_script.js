document.addEventListener('DOMContentLoaded', function() {
    let burger = document.querySelector('.topnav__burger');
    let menu = document.querySelector('.topnav__menu');
    let body = document.querySelector('body');

    burger.addEventListener('click', function(event) {
        burger.classList.toggle('active');
        menu.classList.toggle('active');
        body.classList.toggle('lock');
    });
});