#!/usr/bin/env python3
from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import tempfile
import subprocess

app = Flask(__name__)
limitter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["10 per second"],
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file:
        with tempfile.NamedTemporaryFile() as tmp:
            path = tmp.name
            file.save(path)
            command = [
                "clamscan",
                "-z",
                "--database=/var/www/flag.ldb",
                "--no-summary",
                path,
            ]
            try:
                result = (
                    subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                    )
                    .stdout.strip("\n")
                    .split(" ")
                )

                if len(result) == 3:
                    matched = result[1]
                    return render_template("result.html", matched=matched)
                else:
                    return render_template("result.html", matched=None)
            except Exception as e:
                return f"Something went wrong: {e}", 500

    return "Something went wrong", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
