document.addEventListener('DOMContentLoaded', async() => {
    const token = new URLSearchParams(window.location.search).get('token');
    if (!token) {
        document.getElementById('flagContainer').innerHTML = "<p>No token provided. You need to <a href='/login?next=/'>login</a> .</p>";
        return;
    }

    try {
        const response = await fetch('/flag', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('flagContainer').innerText = result.flag;
        } else {
            document.getElementById('flagContainer').innerText = result.error;
        }
    } catch (error) {
        document.getElementById('flagContainer').innerText = 'Error fetching flag.';
    }
});
