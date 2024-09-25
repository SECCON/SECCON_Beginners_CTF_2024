const loginWorker = new Worker('login.js');

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    loginWorker.postMessage({ username, password });
}

loginWorker.onmessage = function(event) {
    const { token, error } = event.data;
    if (error) {
        document.getElementById('errorContainer').innerText = error;
        return;
    }
    if (token) {
        const params = new URLSearchParams(window.location.search);
        const next = params.get('next');

        if (next) {
            window.location.href = next.includes('token=') ? next: `${next}#token=${token}`;
        } else {
            window.location.href = `/#token=${token}`;
        }
    }
};
