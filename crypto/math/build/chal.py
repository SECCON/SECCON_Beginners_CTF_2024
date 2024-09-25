from Crypto.Util.number import bytes_to_long, isPrime
from secret import x, p, q
import gmpy2


def is_square(n: int):
    return gmpy2.isqrt(n) ** 2 == n


assert isPrime(p)
assert isPrime(q)
assert p != q

a = p - x
b = q - x
assert is_square(x) and is_square(a) and is_square(b)

n = p * q
e = 65537
flag = b"ctf4b{c0u1d_y0u_3nj0y_7h3_m4theM4t1c5?}"
mes = bytes_to_long(flag)
c = pow(mes, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"cipher = {c}")
print(f"ab = {a * b}")
