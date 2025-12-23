// frontend/www/assets/js/modules/attendance.js

document.addEventListener("DOMContentLoaded", () => {
    const totalEl = document.getElementById("totalClasses");
    const attendedEl = document.getElementById("attendedClasses");
    const percentageEl = document.getElementById("attendancePercentage");
    const neededEl = document.getElementById("classesNeeded");
    const statusEl = document.getElementById("statusBadge");

    async function loadAttendance() {
        const user = JSON.parse(localStorage.getItem("user") || "null");

        if (!user || !user.id) {
            window.location.href = "/pages/login.html";
            return;
        }

        // Display dummy attendance data for all users
        const dummyData = {
            total_classes: 120,
            attended_classes: 72,
            classes_needed: 18,
            percentage: 60,
            status: "At Risk"
        };

        // Populate the UI with dummy data
        totalEl.textContent = dummyData.total_classes;
        attendedEl.textContent = dummyData.attended_classes;
        percentageEl.textContent = `${dummyData.percentage}%`;
        neededEl.textContent = dummyData.classes_needed;

        // Set status badge with appropriate styling
        statusEl.textContent = dummyData.status;
        statusEl.className = "status-badge status-danger"; // "At Risk" uses danger styling
    }

    loadAttendance();
});
