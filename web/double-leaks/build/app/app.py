from flask import Flask, request, jsonify, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
import hashlib
import os
import sys
import string
import traceback

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per second"],
)


def get_mongo_client():
    client = MongoClient(host="mongodb", port=27017)
    out = client.db_name.command("ping")
    assert "ok" in out, "MongoDB is not ready"
    return client


# insert init data
try:
    client = get_mongo_client()
    db = client.get_database("double-leaks")
    users_collection = db.get_collection("users")

    admin_username = os.getenv("ADMIN_USERNAME", "")
    assert len(admin_username) > 0 and any(
        [ch in string.printable for ch in admin_username]
    ), "ADMIN_USERNAME is not set"
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    assert len(admin_password) > 0 and any(
        [ch in string.printable for ch in admin_password]
    ), "ADMIN_PASSWORD is not set"
    flag = os.getenv("FLAG", "flag{dummy_flag}")
    assert len(flag) > 0 and any(
        [ch in string.printable for ch in flag]
    ), "FLAG is not set"

    if users_collection.count_documents({}) == 0:
        hashed_password = hashlib.sha256(admin_password.encode("utf-8")).hexdigest()
        users_collection.insert_one(
            {"username": admin_username, "password_hash": hashed_password}
        )
except Exception:
    traceback.print_exc(file=sys.stderr)
finally:
    client.close()


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


@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "page not found :(")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password_hash = request.json["password_hash"]
    if waf(password_hash):
        return jsonify({"message": "DO NOT USE STRANGE WORDS :rage:"}), 400

    try:
        client = get_mongo_client()
        db = client.get_database("double-leaks")
        users_collection = db.get_collection("users")
        user = users_collection.find_one(
            {"username": username, "password_hash": password_hash}
        )
        if user is None:
            return jsonify({"message": "Invalid Credential"}), 401

        # Confirm if credentials are valid just in case :smirk:
        if user["username"] != username or user["password_hash"] != password_hash:
            return jsonify({"message": "DO NOT CHEATING"}), 401

        return jsonify(
            {"message": f"Login successful! Congrats! Here is the flag: {flag}"}
        )

    except Exception:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        client.close()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=41413)
