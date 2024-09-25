import os
from ptrlib import remote, process
from gmpy2 import iroot
from Crypto.Util.number import *
# https://github.com/jvdsn/crypto-attacks/blob/master/shared/polynomial.py
from shared.polynomial import fast_polynomial_gcd

HOST = os.getenv("SECCON_HOST", "localhost")
PORT = int(os.getenv("SECCON_PORT", "5000"))

def resultant(f1, f2, var):
    return Matrix(f1.sylvester_matrix(f2, var)).determinant()

flag17 = []
ns = []

for i in range(17):
    #io = process(["python3", "chall.py"], cwd="../files")
    io = remote(HOST, PORT)
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    exec(io.recvline().decode())
    io.close()

    PR.<m,s> = PolynomialRing(Zmod(n))
    f1 = (m + s)^e - c1
    f2 = (m + s*t1)^e - c2
    f3 = (m*t2 + s)^e - c3
    
    f12 = resultant(f1,f2,s)
    f13 = resultant(f1,f3,s)
    f = fast_polynomial_gcd(f12.univariate_polynomial(),f13.univariate_polynomial())
    print(f)
    flag17.append(int(-f[0]))
    ns.append(int(n))

m17 = CRT(flag17,ns)
print(long_to_bytes(int(iroot(int(m17),17)[0])))
