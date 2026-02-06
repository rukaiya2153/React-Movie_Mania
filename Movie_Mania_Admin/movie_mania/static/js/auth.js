function getToken() {
    return localStorage.getItem("access");
}

function authFetch(url, options = {}) {
    return fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        }
    }).then(res => {
        if (res.status === 401) {
            logout();
        }
        return res.json();
    });
}

function logout() {
    localStorage.clear();
    window.location.href = "/login.html";
}

function go(page) {
    window.location.href = "/" + page;
}
