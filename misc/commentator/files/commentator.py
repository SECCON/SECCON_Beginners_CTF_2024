#!/usr/local/bin/python

import os
import uuid

############################## Logo ##############################
print(
    f"""                                          _        _                  __
  ___ ___  _ __ ___  _ __ ___   ___ _ __ | |_ __ _| |_ ___  _ __   _  \\ \\
 / __/ _ \\| '_ ` _ \\| '_ ` _ \\ / _ \\ '_ \\| __/ _` | __/ _ \\| '__| (_)  | |
| (_| (_) | | | | | | | | | | |  __/ | | | || (_| | || (_) | |     _   | |
 \\___\\___/|_| |_| |_|_| |_| |_|\\___|_| |_|\\__\\__,_|\\__\\___/|_|    (_)  | |
                                                                      /_/
{"-" * 75}
Enter your Python code (ends with __EOF__)"""
)
############################## Logo ##############################

python = ""
while True:
    line = input(">>> ").replace("\r", "")
    if "__EOF__" in line:
        python += 'print("thx :)")'
        break
    python += f"# {line}\n"  # comment :)

pyfile = f"/tmp/{uuid.uuid4()}.py"
with open(pyfile, "w") as f:
    f.write(python)

os.system(f"python {pyfile}")
os.remove(pyfile)
