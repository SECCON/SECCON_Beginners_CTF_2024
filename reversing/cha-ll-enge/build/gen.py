flag = "ctf4b{7ick_7ack_11vm_int3rmed14te_repr3sen7a7i0n}\0"

answer = []

answer.append(ord("w"))

for i in range(len(flag) - 1):
    answer.append(answer[i] ^ ord(flag[i]))

print(len(flag), len(answer))
print(answer)

# [119, 20, 96, 6, 50, 80, 43, 28, 117, 22, 125, 34, 21, 116, 23, 124, 35, 18, 35, 85, 56, 103, 14, 96, 20, 39, 85, 56, 93, 57, 8, 60, 72, 45, 114, 0, 101, 21, 103, 84, 39, 66, 44, 27, 122, 77, 36, 20, 122, 7]
