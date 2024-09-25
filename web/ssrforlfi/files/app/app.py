import os
import re
import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def ssrforlfi():
    url = request.args.get("url")
    if not url:
        return "Welcome to Website Viewer.<br><code>?url=http://example.com/</code>"

    # Allow only a-z, ", (, ), ., /, :, ;, <, >, @, |
    if not re.match('^[a-z"()./:;<>@|]*$', url):
        return "Invalid URL ;("

    # SSRF & LFI protection
    if url.startswith("http://") or url.startswith("https://"):
        if "localhost" in url:
            return "Detected SSRF ;("
    elif url.startswith("file://"):
        path = url[7:]
        if os.path.exists(path) or ".." in path:
            return "Detected LFI ;("
    else:
        # Block other schemes
        return "Invalid Scheme ;("

    try:
        # RCE ?
        proc = subprocess.run(
            f"curl '{url}'",
            capture_output=True,
            shell=True,
            text=True,
            timeout=1,
        )
    except subprocess.TimeoutExpired:
        return "Timeout ;("
    if proc.returncode != 0:
        return "Error ;("
    return proc.stdout


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4989)
