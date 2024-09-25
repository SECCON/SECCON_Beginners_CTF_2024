import os
import shutil
import time
import uuid

from flask import Flask, render_template, request, session, redirect
from qiling import Qiling
from qiling.const import QL_ARCH, QL_OS, QL_VERBOSE
from qiling.extensions import pipe

from pwn import asm

app = Flask(__name__)

app.secret_key = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    if "id" not in session:
        session["id"] = "1"
    return render_template("index.html", id=session["id"])


@app.route("/reset", methods=["GET"])
def reset():
    session["id"] = "1"
    return redirect("/")


@app.route("/", methods=["POST"])
def submit():
    code = request.form["code"]
    if len(code.strip()) == 0:
        return render_template("index.html", id=session["id"], error="Please input the code.")
    if ";" in code:
        return render_template("index.html", id=session["id"], error="Please remove the semicolon.")
    lines = code.splitlines()
    if len(lines) > 25:
        return render_template(
            "index.html",
            id=session["id"],
            error="Too many instructions. Please use less than 25 instructions.",
        )
    for line in lines:
        try:
            order = line.split()[0]
            if order not in ["mov", "push", "syscall"]:
                return render_template(
                    "index.html",
                    id=session["id"],
                    error="Invalid instructions are included. Please use only mov, push, syscall.",
                )
        except Exception:
            continue

    try:
        asm_code = asm(code, arch="amd64", os="linux")
    except Exception:
        return render_template(
            "index.html", id=session["id"], error="Failed to assemble the code. Please check the code."
        )

    # Debug
    logpath = os.path.join("logs", str(time.time()) + ".log")
    logf = open(logpath, "w")
    logf.write(code + "\n" * 2)
    logf.close()

    dirname = str(uuid.uuid4())
    os.mkdir(dirname)
    if session["id"] == "4":
        f = open(os.path.join(dirname, "flag.txt"), "w")
        flag = os.environ.get("FLAG", "ctf4b{fake_flag}")
        f.write(flag)
        f.close()
    ql = Qiling(
        code=asm_code,
        rootfs=dirname,
        archtype=QL_ARCH.X8664,
        ostype=QL_OS.LINUX,
        verbose=QL_VERBOSE.DEFAULT,
        log_file=logpath,
    )

    ql.os.stdout = pipe.SimpleOutStream(0)

    try:
        ql.run()
    except Exception:
        return render_template(
            "index.html",
            id=session["id"],
            error="Failed to execute the code. Please check the code.",
        )

    shutil.rmtree(dirname, ignore_errors=True)

    try:
        stdout=ql.os.stdout.read(1024).decode().strip()
    except Exception:
        stdout = str(ql.os.stdout.read(1024))

    message = "Successfully executed the code!"
    if session["id"] == "1" and ql.arch.regs.read("rax") == 0x123:
        message = "Congratulation! Let's proceed to the next stage!"
        session["id"] = "2"
    elif session["id"] == "2" and ql.arch.regs.read("rax") == 0x123 and ql.arch.stack_pop() == 0x123:
        message = "Congratulation! Let's proceed to the next stage!"
        session["id"] = "3"
    elif session["id"] == "3" and "Hello" in stdout:
        message = "Congratulation! Let's proceed to the next stage!"
        session["id"] = "4"
    elif session["id"] == "4" and os.getenv("FLAG", "ctf4b{fake_flag}") in stdout:
        message = "Congratulation! You have completed all stages!"

    return render_template(
        "index.html",
        id=session["id"],
        message=message,
        stdout=stdout,
        rax=hex(ql.arch.regs.read("rax")),
        rbx=hex(ql.arch.regs.read("rbx")),
        rcx=hex(ql.arch.regs.read("rcx")),
        rdx=hex(ql.arch.regs.read("rdx")),
        rsi=hex(ql.arch.regs.read("rsi")),
        rdi=hex(ql.arch.regs.read("rdi")),
        rbp=hex(ql.arch.regs.read("rbp")),
        rip=hex(ql.arch.regs.read("rip")),
        rsp=hex(ql.arch.regs.read("rsp")),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
