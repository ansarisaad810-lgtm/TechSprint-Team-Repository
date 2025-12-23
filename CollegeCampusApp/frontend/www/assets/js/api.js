const BACKEND_BASE = "http://127.0.0.1:5000";

function _authHeaders() {
    const token = localStorage.getItem("token");
    return token ? { "Authorization": `Bearer ${token}` } : {};
}

async function _handleResponse(response) {
    if (response.status === 401 || response.status === 422) {
        localStorage.clear();
        window.location.href = "/pages/login.html";
        return null;
    }
    try {
        return await response.json();
    } catch {
        return null;
    }
}

async function apiGet(endpoint) {
    const response = await fetch(`${BACKEND_BASE}${endpoint}`, {
        headers: _authHeaders()
    });
    return _handleResponse(response);
}

async function apiPost(endpoint, data, isForm = false) {
    const opts = {
        method: "POST",
        headers: {},
    };

    if (isForm) {
        // For FormData, let the browser set Content-Type boundary
        opts.body = data;
        opts.headers = _authHeaders();
    } else {
        opts.body = JSON.stringify(data);
        opts.headers = { "Content-Type": "application/json", ..._authHeaders() };
    }

    const response = await fetch(`${BACKEND_BASE}${endpoint}`, opts);
    return _handleResponse(response);
}
