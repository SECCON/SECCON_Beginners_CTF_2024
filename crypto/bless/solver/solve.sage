import json
from tqdm import tqdm

p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
q = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
F1 = GF(p)
E1 = EllipticCurve(F1, (0, 4))
G1 = E1(0x17F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB, 0x08B3F481E3AAA0F1A09E30ED741D8AE4FCF5E095D5D00AF600DB18CB2C04B3EDD03CC744A2888AE40CAA232946C5E7E1)
k = 12
assert (p^k - 1) % q == 0

F2 = GF(p^2, 'l', modulus=x^2+1)
l = F2.gen()
E2 = EllipticCurve(F2, (0, 4*(1 + l)))

F12 = GF(p^12, 'w', modulus=x^12-2*x^6+2)
w = F12.gen()
E12 = EllipticCurve(F12, (0, 4))

with open("../files/output.json", "r") as f:
    challenges = json.load(f)

def from_dict(P):
    if isinstance(P['x'], int):
        return E1(F1(P['x']), F2(P['y']))
    else:
        return E2(
            F2(P['x'][0]) + F2(P['x'][1]) * l,
            F2(P['y'][0]) + F2(P['y'][1]) * l
        )

def twist(Px, Py):
    z = w^-1
    a, b = list(Px.polynomial())
    Px = a + b * (w^6 - 1)
    a, b = list(Py.polynomial())
    Py = a + b * (w^6 - 1)
    return z^2 * F12(Px), z^3 * F12(Py)

G12 = E12(G1[0], G1[1])
flag = ''
for chall in tqdm(challenges):
    P, Q, R = from_dict(chall['P']), from_dict(chall['Q']), from_dict(chall['R'])

    # Twist
    P12 = E12(P[0], P[1])
    Q12 = E12(twist(Q[0], Q[1]))
    mu1 = P12.tate_pairing(Q12, n=q, k=k)

    R12 = E12(twist(R[0], R[1]))
    mu2 = G12.tate_pairing(R12, n=q, k=k)

    for c in range(0x20, 0x7f):
        if mu1 ** c == mu2:
            flag += chr(c)
            tqdm.write("FLAG: " + flag)
            break
    else:
        tqdm.write("Something went wrong...")
        exit(1)
