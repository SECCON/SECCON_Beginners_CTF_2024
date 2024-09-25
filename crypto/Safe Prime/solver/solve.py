from ptrlib import *

exec(open("../files/output.txt", "r").read())

# n = p(2p+1)
# 2p^2 + p - n = 0
# p = (-1 + sqrt(1 + 8n)) / 4
p = (root(1 + 8*n, 2) - 1) // 4
q = 2 * p + 1
d = pow(65537, -1, (p-1)*(q-1))

m = pow(c, d, n)
print(int.to_bytes(m, 1024//8, 'big').lstrip(b'\x00'))

