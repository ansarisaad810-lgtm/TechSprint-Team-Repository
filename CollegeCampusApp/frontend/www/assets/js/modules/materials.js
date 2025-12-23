// frontend/www/assets/js/modules/materials.js

// Global variables
let allMaterials = [];
let currentFilter = 'All';

// Load materials on page load
document.addEventListener("DOMContentLoaded", async () => {
    await loadMaterials();
});

// Load all materials from backend
async function loadMaterials() {
    try {
        const res = await apiGet("/materials/list");
        allMaterials = res || [];
        renderMaterials(allMaterials);
    } catch (error) {
        console.error("Error loading materials:", error);
        showToast("Error loading materials", "error");
    }
}

// Render materials to the grid
function renderMaterials(materials) {
    const container = document.getElementById("materialsList");

    if (!materials || materials.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📚</div>
                <p>No materials found.</p>
                <p style="font-size: 0.875rem; color: #64748b; margin-top: 0.5rem;">
                    ${allMaterials.length === 0 ? 'Upload your first material!' : 'Try a different search or filter.'}
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = materials.map(material => `
        <div class="material-card">
            <div class="material-icon">${getFileIcon(material.filename)}</div>
            <div class="material-title">${escapeHtml(material.title)}</div>
            <div class="material-course">${escapeHtml(material.course || 'General')}</div>
            <div class="material-description">${escapeHtml(material.description || 'No description available')}</div>
            <div class="material-meta">
                <span class="material-type">${escapeHtml(material.type)}</span>
                <span>${formatFileSize(material.size)}</span>
            </div>
            <button class="download-btn" onclick="downloadMaterial('${escapeHtml(material.filename)}')">
                📥 Download
            </button>
        </div>
    `).join('');
}

// Upload material
async function uploadMaterial(event) {
    event.preventDefault();

    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);

    try {
        const response = await fetch('/materials/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showToast("Material uploaded successfully!", "success");
            form.reset();
            await loadMaterials();
        } else {
            showToast(result.error || "Upload failed", "error");
        }
    } catch (error) {
        console.error("Upload error:", error);
        showToast("Error uploading material", "error");
    }
}

// Live search filter - triggers on every keyup
function filterMaterials() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.toLowerCase().trim();

    // Filter materials based on search term
    let filtered = allMaterials;

    if (searchTerm) {
        filtered = allMaterials.filter(material => {
            // Search in title, course, description, and filename
            const title = (material.title || '').toLowerCase();
            const course = (material.course || '').toLowerCase();
            const description = (material.description || '').toLowerCase();
            const filename = (material.filename || '').toLowerCase();

            return title.includes(searchTerm) ||
                course.includes(searchTerm) ||
                description.includes(searchTerm) ||
                filename.includes(searchTerm);
        });
    }

    // Apply type filter if not "All"
    if (currentFilter !== 'All') {
        filtered = filtered.filter(material => material.type === currentFilter);
    }

    renderMaterials(filtered);
}

// Filter by type
function filterByType(type) {
    currentFilter = type;

    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Apply filter
    filterMaterials();
}

// Download material
function downloadMaterial(filename) {
    window.location.href = `/materials/download/${encodeURIComponent(filename)}`;
}

// Helper: Get file icon based on extension
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'txt': '📄',
        'ppt': '📊',
        'pptx': '📊',
        'xlsx': '📗',
        'xls': '📗'
    };
    return icons[ext] || '📄';
}

// Helper: Format file size
function formatFileSize(bytes) {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Helper: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show toast notification
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
