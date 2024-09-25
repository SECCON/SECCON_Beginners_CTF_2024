import random 
import string

TEMPLATE = '''
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int i = 0;

__attribute__((constructor(101))) 
void func_e0db2736(int argc, char **argv) {
	if (argc != 2) {
		puts("usage: construct <password>");
		_exit(1);
	}
}

__attribute__((constructor(102))) 
void func_f8db6e92(int argc, char **argv) {
	if (strlen(argv[1]) != %FLAG_LEN%) exit(1);
}

%FUNCTIONS%

int main(int argc, char **argv) {
	puts("CONGRATULATIONS!");
    printf("The flag is ctf4b{%s}\\n", argv[1]);
	_exit(0);
}

__attribute__((destructor))
void func_dc69ef50() {
	puts("WRONG");
}
'''

TEMPLATE_FUNC = '''
__attribute__((constructor(%INDEX_CTOR%)))
void func_%FUNC_NAME%(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"%CHARS%"[i], 2) != 0) exit(1);
    i += 2;
}
'''


def random_func_name() -> str:
    return ''.join(random.sample('0123456789abcdef', 8))


def gen_func(index: int, chunk: str) -> str:
    FLAG_CHARS = string.ascii_lowercase + string.digits + '_'
    FLAG_CHARS = [c for c in FLAG_CHARS if c not in chunk]
    chars = ''.join(random.sample(FLAG_CHARS, len(FLAG_CHARS)))
    chars = chars[:index*2] + chunk + chars[index*2:]
    return TEMPLATE_FUNC.replace('%INDEX_CTOR%', str(103 + index)).replace('%FUNC_NAME%', random_func_name()).replace('%CHARS%', chars)


flag = 'c0ns7ruc70rs_3as3_h1d1ng_7h1ngs!'
assert len(flag) % 2 == 0

flag_chunks = [flag[i:i+2] for i in range(0, len(flag), 2)]
functions = [gen_func(i, c) for (i, c) in random.sample(list(enumerate(flag_chunks)), len(flag_chunks))]
print(TEMPLATE.replace('%FLAG_LEN%', str(len(flag))).replace('%FUNCTIONS%', '\n'.join(functions)))
