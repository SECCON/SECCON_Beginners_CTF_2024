import requests
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "8080"))

try:
    url = "http://{}:{}/".format(HOST, PORT)
    if HOST != "localhost":
        url = "https://{}/".format(HOST)
    print("URL:", url)

    # fetch cookie in top page
    res = requests.get(url, timeout=10)

    # post challenge 1
    data = {
        "code": "mov rax, 0x123",
    }
    cookies = {
        "session": res.cookies.get("session"),
    }
    res = requests.post(url, data=data, cookies=cookies, timeout=10)
    print("challenge 1 is solved.")

    # post challenge 2
    data = {
        "code": "mov rax, 0x123\npush rax",
    }
    cookies = {
        "session": res.cookies.get("session"),
    }
    res = requests.post(url, data=data, cookies=cookies, timeout=10)
    print("challenge 2 is solved.")

    # post challenge 3
    data = {
        "code": "mov  rax, 0x6f6c6c6548\npush rax\nmov  rax, 1\nmov  rdi, 1\nmov  rsi, rsp\nmov  rdx, 5\nsyscall",
    }
    cookies = {
        "session": res.cookies.get("session"),
    }
    res = requests.post(url, data=data, cookies=cookies, timeout=10)
    print("challenge 3 is solved.")

    # post challenge 4
    data = {
        "code": "mov  rax, 0\npush rax\nmov  rax, 0x7478742e67616c66\npush rax\nmov  rdi, rsp\nmov  rsi, 0\nmov  rax, 2\nsyscall\nmov  rdi, rax\nmov  rsi, rsp\nmov  rdx, 1024\nmov  rax, 0\nsyscall\nmov  rdx, rax\nmov  rsi, rsp\nmov  rdi, 1\nmov  rax, 1\nsyscall",
    }
    cookies = {
        "session": res.cookies.get("session"),
    }
    res = requests.post(url, data=data, cookies=cookies, timeout=10)
    print("challenge 4 is solved.")
    print(res.text)

except Exception as e:
    print(e)
