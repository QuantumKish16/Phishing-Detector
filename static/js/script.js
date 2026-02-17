document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       THEME TOGGLE
    ========================== */

    const toggleBtn = document.getElementById("themeToggle");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark");

            if (document.body.classList.contains("dark")) {
                toggleBtn.textContent = "☀️";
                localStorage.setItem("theme", "dark");
            } else {
                toggleBtn.textContent = "🌙";
                localStorage.setItem("theme", "light");
            }
        });

        // Load saved theme
        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark");
            toggleBtn.textContent = "☀️";
        }
    }


    /* =========================
       SECURITY SCORE
    ========================== */

    window.updateScore = function(score) {
        const meter = document.getElementById("meterFill");
        const text = document.getElementById("scoreText");

        if (!meter || !text) return;

        meter.style.width = score + "%";
        text.textContent = score + "%";

        if (score > 70) {
            meter.style.background = "green";
        } else if (score > 40) {
            meter.style.background = "orange";
        } else {
            meter.style.background = "red";
        }
    };

});
