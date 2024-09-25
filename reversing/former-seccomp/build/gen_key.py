key = 'ctf4b:2024'

enc_key = []
for i in range(len(key)):
  enc_key.append(ord(key[i]) ^ (0x20 + i))

print('{' + ', '.join([hex(c) for c in enc_key]) +'}')
