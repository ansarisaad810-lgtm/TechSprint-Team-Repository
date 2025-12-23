// frontend/www/assets/js/auth.js

const AUTH_BASE = "http://127.0.0.1:5000/api/auth";

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const erp = document.getElementById("erp").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("loginMessage");

    if (!erp || !password) {
        msg.innerText = "ERP ID and password are required.";
        return;
    }

    try {
        const response = await fetch(`${AUTH_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ erp, password })
        });

        const data = await response.json();

        if (!response.ok) {
            msg.innerText = data.message || "Login failed.";
            return;
        }

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        window.location.href = "/pages/dashboard.html";

    } catch (err) {
        console.error(err);
        msg.innerText = "Server not reachable.";
    }
});
