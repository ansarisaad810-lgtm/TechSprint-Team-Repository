// frontend/www/assets/js/app.js

function navigate(page) {
    window.location.href = "pages/" + page;
}

function goTo(page) {
    window.location.href = page;
}

document.addEventListener("deviceready", function () {
    console.log("Cordova ready");
}, false);
