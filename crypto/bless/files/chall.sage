import json
import os

FLAG = os.getenv("FLAG", "ctf4b{*** REDACTED ***}").encode()

# https://neuromancer.sk/std/bls/BLS12-381
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
q = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
F1 = GF(p)
E1 = EllipticCurve(F1, (0, 4))
G1 = E1(0x17F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB, 0x08B3F481E3AAA0F1A09E30ED741D8AE4FCF5E095D5D00AF600DB18CB2C04B3EDD03CC744A2888AE40CAA232946C5E7E1)

F2 = GF(p^2, 'x', modulus=x^2+1)
E2 = EllipticCurve(F2, (0, 4*(1+F2.gen())))
G2 = E2.random_point()

def to_dict(P):
    if P.base_ring() == F1:
        return {'x': int(P[0]), 'y': int(P[1])}
    else:
        Px, Py = P[0].polynomial(), P[1].polynomial()
        return {'x': [int(Px[0]), int(Px[1])], 'y': [int(Py[0]), int(Py[1])]}

challenges = []
for c in FLAG:
    s, t = randrange(q), randrange(q)
    challenges.append({
        'P': to_dict(s*G1),
        'Q': to_dict(t*G2),
        'R': to_dict(c*s*t*G2)
    })

with open("output.json", "w") as f:
    json.dump(challenges, f)
