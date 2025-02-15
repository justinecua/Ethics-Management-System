
let LogoutBTN = document.getElementById('LogoutBTN');
let ModalLogoutOverlay = document.getElementById('Logout-Overlay');
let LCBack = document.getElementById('LC-Back');

LCBack.addEventListener('click', function () {
    ModalLogoutOverlay.style.display = "none";
});

LogoutBTN.addEventListener('click', function () {
    ModalLogoutOverlay.style.display = "flex";
});
