#!/usr/local/bin/python
import os
from Crypto.Util.number import *
from random import randint
FLAG = os.getenv("FLAG", "ctf4b{*** REDACTED ***}").encode()

e, nbit = 17, 512
m = bytes_to_long(FLAG)

p, q = getPrime(nbit), getPrime(nbit)
n = p * q

assert m < n

s = randint(0, 2**nbit)
t1, t2 = randint(0, 2**nbit), randint(0, 2**nbit)

c1 = pow(m + s, e, n)
c2 = pow(m + s * t1, e, n)
c3 = pow(m * t2 + s, e, n)

print(f"{e=}")
print(f"{n=}")
print(f"{t1=}")
print(f"{t2=}")
print(f"{c1=}")
print(f"{c2=}")
print(f"{c3=}")
