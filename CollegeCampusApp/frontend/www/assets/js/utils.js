// frontend/www/assets/js/utils.js

/**
 * Format a date as YYYY-MM-DD
 * @param {Date} date
 * @returns {string}
 */
function formatDate(date) {
    const d = new Date(date);
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    const year = d.getFullYear();
    return `${year}-${month}-${day}`;
}

/**
 * Show an alert message
 * @param {string} message
 * @param {string} type - "success", "error", "info"
 */
function showAlert(message, type = "info") {
    const alertBox = document.createElement("div");
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    document.body.appendChild(alertBox);
    setTimeout(() => alertBox.remove(), 3000);
}

/**
 * Validate if a string is empty
 * @param {string} str
 * @returns {boolean}
 */
function isEmpty(str) {
    return !str || str.trim().length === 0;
}
