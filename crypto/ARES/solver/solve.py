import os
from ptrlib import *

PORT = int(os.getenv("SECCON_PORT", "5000"))
HOST = os.getenv("SECCON_HOST", "localhost")

def encrypt(m: int):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("m: ", m)
    return bytes.fromhex(sock.recvlineafter("c: ").decode())

def decrypt(c: bytes):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("c: ", c.hex())
    return int(sock.recvlineafter("m: "))

def lift(c: int):
    c = pow(c, e, n)
    return int.to_bytes(c, 1024//8, 'big')

while True:
    #sock = Process(["python", "server.py"], cwd="../files")
    sock = Socket(HOST, PORT)

    enc_flag = bytes.fromhex(sock.recvlineafter(": ").decode())

    e = 65537
    n = decrypt(encrypt(-1)) + 1

    tmp = encrypt(31337)
    iv, enc = tmp[:16], tmp[16:]
    dec = lift(decrypt(iv + enc))

    for i in range(1024//8-16, -16, -16):
        new_block = xor(enc[i-16:i], xor(dec[i:i+16], enc_flag[i:i+16]))
        enc = b"\x00"*(i-16) + new_block + enc[i:]
        tmp = decrypt(iv + enc)
        dec = lift(tmp)

    iv = xor(iv, xor(dec[:16], enc_flag[:16]))
    flag = decrypt(iv + enc)
    flag = int.to_bytes(flag, 1024//8, 'big')[:-16]

    if b"ctf4" in flag:
        print(flag.decode())
        exit()

    logger.warning("Bad luck!")
