const music = document.getElementById("music");
const btn = document.getElementById("musicBtn");

btn.addEventListener("click", function () {

    if (music.paused) {

        music.play();

        btn.innerHTML = "⏸ Pause Music";

    } else {

        music.pause();

        btn.innerHTML = "▶ Play Music";

    }

});