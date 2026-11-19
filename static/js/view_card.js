const music = document.getElementById("music");
const musicBtn = document.getElementById("musicBtn");

let musicPlaying = false;

if (musicBtn) {
    musicBtn.addEventListener("click", () => {
        if (musicPlaying) {
            music.pause();
            musicBtn.innerHTML = "🎵 Music";
            musicPlaying = false;
        } else {
            music.play();
            musicBtn.innerHTML = "⏸ Pause";
            musicPlaying = true;
        }
    });
}

function popBalloon(balloon) {
    balloon.classList.add("pop");

    confetti({
        particleCount: 25,
        spread: 60,
        origin: { y: 0.8 }
    });

    setTimeout(() => {
        balloon.remove();
    }, 400);
}

function openSurprise() {
    const surpriseOverlay = document.getElementById("surpriseOverlay");
    const letterOverlay = document.getElementById("letterOverlay");

    if (letterOverlay) {
        letterOverlay.style.display = "none";
    }

    if (surpriseOverlay) {
        surpriseOverlay.style.display = "grid";
    }

    document.body.style.overflow = "hidden";

    confetti({
        particleCount: 260,
        spread: 180,
        origin: { y: 0.6 }
    });
}

function closeSurprise() {
    const surpriseOverlay = document.getElementById("surpriseOverlay");
    const letterOverlay = document.getElementById("letterOverlay");

    if (surpriseOverlay) {
        surpriseOverlay.style.display = "none";
    }

    if (letterOverlay) {
        letterOverlay.style.display = "none";
    }

    document.body.style.overflow = "auto";
}

function closeSurpriseOnBackdrop(event) {
    if (event.target.id === "surpriseOverlay") {
        closeSurprise();
    }
}

function openLetter() {
    const letterOverlay = document.getElementById("letterOverlay");

    if (letterOverlay) {
        letterOverlay.style.display = "grid";
    }

    document.body.style.overflow = "hidden";

    confetti({
        particleCount: 180,
        spread: 120,
        origin: { y: 0.6 }
    });
}

function closeLetter() {
    const letterOverlay = document.getElementById("letterOverlay");

    if (letterOverlay) {
        letterOverlay.style.display = "none";
    }

    document.body.style.overflow = "hidden";
}

function closeLetterOnBackdrop(event) {
    if (event.target.id === "letterOverlay") {
        closeLetter();
    }
}

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeSurprise();
    }
});