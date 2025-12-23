// frontend/www/assets/js/modules/lostfound.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("lostFoundForm");
    const itemsList = document.getElementById("itemsList");
    const mediaInput = document.getElementById('media');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    if (mediaInput && fileNameDisplay) {
        mediaInput.addEventListener('change', () => {
            const f = mediaInput.files[0];
            fileNameDisplay.textContent = f ? f.name : 'Click to upload or drag and drop';
        });
    }

    async function loadItems() {
        itemsList.innerHTML = "<p>Loading items...</p>";

        const res = await apiGet("/lostfound/list");
        if (!res || res.length === 0) {
            itemsList.innerHTML = "<p>No items reported yet.</p>";
            // Ensure container is visible
            const container = document.getElementById("itemsContainer");
            if (container) container.style.display = "block";
            return;
        }

        itemsList.innerHTML = "";

        // Ensure container is visible
        const container = document.getElementById("itemsContainer");
        if (container) container.style.display = "block";

        res.forEach(item => {
            const card = document.createElement("div");
            card.className = "item-card";

            card.innerHTML = `
                <div class="menu-container">
                    <button class="menu-trigger" onclick="event.stopPropagation(); toggleCardMenu(this)">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="12" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </button>
                    <div class="menu-dropdown">
                        <button class="menu-item remove" onclick="event.stopPropagation(); deleteItem(${item.id})">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M3 6h18"></path>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                            Remove
                        </button>
                    </div>
                </div>
                <img src="${item.media_path}" alt="Item Image" onerror="this.style.display='none'">
                <div style="padding: 0 1.5rem 1.5rem 1.5rem;">
                    <h3 style="color: white; font-size: 1.125rem; margin-bottom: 0.5rem;">${item.item_name}</h3>
                    <div style="display: flex; align-items: center; gap: 0.5rem; color: #cbd5e1; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        <span>📍</span>
                        <span>${item.location || 'Unknown Location'}</span>
                    </div>
                    <p style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 1rem; line-height: 1.5;">
                        ${item.description || "No description provided."}
                    </p>
                    <div style="border-top: 1px solid #334155; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
                         <span style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">
                            ${item.status}
                         </span>
                         <span style="color: #64748b; font-size: 0.75rem;">
                            ID: ${item.id}
                         </span>
                    </div>
                </div>
            `;

            itemsList.appendChild(card);
        });
    }

    // Menu logic
    window.toggleCardMenu = (btn) => {
        // Close all other menus first
        document.querySelectorAll('.menu-dropdown.active').forEach(m => {
            if (m !== btn.nextElementSibling) m.classList.remove('active');
        });
        btn.nextElementSibling.classList.toggle('active');
    };

    // Close menu when clicking outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.menu-dropdown.active').forEach(m => m.classList.remove('active'));
    });

    // Delete item logic
    window.deleteItem = async (itemId) => {
        if (!confirm("Are you sure you want to remove this item?")) return;

        try {
            const res = await fetch(`/lostfound/remove/${itemId}`, {
                method: 'DELETE'
            });

            const result = await res.json();
            if (res.ok) {
                showToast("Item removed successfully", "success");
                loadItems();
            } else {
                showToast(result.error || "Failed to remove item", "error");
            }
        } catch (error) {
            console.error("Delete error:", error);
            showToast("Error removing item", "error");
        }
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const user = JSON.parse(localStorage.getItem("user") || "null");
        if (!user) {
            window.location.href = "/pages/login.html";
            return;
        }

        const formData = new FormData();
        formData.append("uploader_id", user.id);
        formData.append("item_name", document.getElementById("item_name").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("location", document.getElementById("location").value);
        formData.append("media", document.getElementById("media").files[0]);

        try {
            // Use relative URL to match materials.js pattern
            const response = await fetch('/lostfound/report', {
                method: 'POST',
                body: formData
            });

            // Handle response exactly like materials.js (expecting JSON)
            // But with added safety for the 500 error case
            const responseText = await response.text();
            let result;
            try {
                result = JSON.parse(responseText);
            } catch (e) {
                console.error("Non-JSON response:", responseText);
                showToast("Server error: " + responseText.substring(0, 50), "error");
                return;
            }

            if (response.ok && !result.error) {
                showToast("Item reported successfully!", "success");
                form.reset();
                if (fileNameDisplay) fileNameDisplay.textContent = 'Click to upload or drag and drop';
                loadItems();
            } else {
                const errorMsg = result.error || "Failed to submit item";
                showToast(errorMsg, "error");

                // Auto-logout if session is invalid
                if (errorMsg.includes("Invalid User Session")) {
                    setTimeout(() => {
                        localStorage.removeItem("user");
                        localStorage.removeItem("token");
                        window.location.href = "/pages/login.html";
                    }, 1500);
                }
            }
        } catch (error) {
            console.error("Submission error:", error);
            showToast("Error submitting item", "error");
        }
    });

    // Helper: Show toast notification (copied from materials.js)
    function showToast(message, type = "success") {
        const existingToast = document.querySelector(".toast");
        if (existingToast) existingToast.remove();

        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    loadItems();
});
