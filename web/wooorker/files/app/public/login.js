let username, password;

onmessage = async function(event) {
    if(!username) username = event.data.username;
    if(!password) password = event.data.password;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const result = await response.json();

        if (response.ok) {
            postMessage({ token: result.token });
        } else {
            postMessage({ token: '', error: result.error });
        }
    } catch (error) {
        postMessage({ token: '', error: 'Error logging in.' });
    }
};
