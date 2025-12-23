// frontend/www/assets/js/modules/timetable.js

function loadTimetable() {
    const sectionSelect = document.getElementById("sectionInput");
    const semesterSelect = document.getElementById("semester");

    const section = sectionSelect.value.trim();
    const semester = semesterSelect.value.trim();

    if (!section || !semester) {
        showToast("Please select both section and semester", "error");
        return;
    }

    // Hide empty state and show timetable container
    const emptyState = document.getElementById("emptyState");
    const timetableContainer = document.getElementById("timetableContainer");

    if (emptyState) emptyState.style.display = "none";
    if (timetableContainer) timetableContainer.style.display = "block";

    // Update section display badge
    const sectionDisplay = document.getElementById("sectionDisplay");
    if (sectionDisplay) {
        sectionDisplay.textContent = `${section} - Semester ${semester}`;
    }

    // Construct image path: "Semester X - Section Y.jpeg"
    const imagePath = `../assets/images/timetables/Semester ${semester} - ${section}.jpeg`;

    // Display the timetable image
    const timetableBody = document.getElementById("timetableBody");
    if (timetableBody) {
        timetableBody.innerHTML = `
            <tr>
                <td colspan="6" style="padding: 0; border: none;">
                    <img src="${imagePath}" 
                         alt="Timetable for ${section} - Semester ${semester}" 
                         style="width: 100%; height: auto; display: block; border-radius: 0.5rem;"
                         onerror="handleImageError(this, '${section}', '${semester}')">
                </td>
            </tr>
        `;
    }

    showToast("Timetable loaded successfully!", "success");
}

function handleImageError(img, section, semester) {
    // If image fails to load, show error message
    const timetableBody = document.getElementById("timetableBody");
    if (timetableBody) {
        timetableBody.innerHTML = `
            <tr>
                <td colspan="6" style="padding: 2rem; text-align: center; color: #94a3b8;">
                    <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">📅</div>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;">Timetable not found</p>
                    <p style="font-size: 0.875rem; color: #64748b;">
                        No timetable image found for ${section} - Semester ${semester}
                    </p>
                    <p style="font-size: 0.75rem; color: #64748b; margin-top: 0.5rem;">
                        Expected file: Semester ${semester} - ${section}.jpeg
                    </p>
                </td>
            </tr>
        `;
    }
    showToast(`Timetable image not found for ${section} - Semester ${semester}`, "error");
}

function resetTimetable() {
    const emptyState = document.getElementById("emptyState");
    const timetableContainer = document.getElementById("timetableContainer");

    if (emptyState) emptyState.style.display = "block";
    if (timetableContainer) timetableContainer.style.display = "none";

    // Reset form
    const form = document.getElementById("timetableForm");
    if (form) form.reset();
}

function showToast(message, type = "success") {
    // Remove existing toast if any
    const existingToast = document.querySelector(".toast");
    if (existingToast) existingToast.remove();

    // Create new toast
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
