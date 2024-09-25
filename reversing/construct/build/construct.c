
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
	if (strlen(argv[1]) != 32) exit(1);
}


__attribute__((constructor(113)))
void func_91e3f562(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"c7l9532k0avfxso4uzipd18egbnyw6rm_tqjh"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(106)))
void func_c285f76d(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"9_xva4uchnkyi6wb2ld507p8g3stfej1rzqmo"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(105)))
void func_b548021f(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"lzau7rvb9qh5_1ops6jg3ykf8x0emtcind24w"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(114)))
void func_af41723c(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"l8s0xb4i1frkv6a92j5eycng3mwpzduqth_7o"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(110)))
void func_1f5eba30(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"17zv5h6wjgbqerastioc294n0lxu38fdk_ypm"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(118)))
void func_da53ce29(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"_k6nj8hyxvzcgr1bu2petf5qwl09ids!om347a"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(111)))
void func_bae805f6(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"1cgovr4tzpnj29ay3_8wk7li6uqfmhe50bdsx"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(108)))
void func_d902e81f(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"tufij3cykhrsl841qo6_0dwg529zanmbpvxe7"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(107)))
void func_74b2a53c(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"r8x9wn65701zvbdfp4ioqc2hy_juegkmatls3"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(116)))
void func_3d90c2fa(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"aj_d29wcrqiok53b7tyn0p6zvfh1lxgum48es"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(115)))
void func_69fd4a70(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"l539rbmoifye0u6dj1pw8nqt_74sz2gkvaxch"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(103)))
void func_9e540c6a(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"c0_d4yk261hbosje893w5igzfrvaumqlptx7n"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(109)))
void func_35efd7b6(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"b0i21csjhqug_3erat9f6mx854pyol7zkvdwn"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(117)))
void func_3b8e07a4(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"3mq16t9yfs842cbvlw5j7k0prohengduzx_ai"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(104)))
void func_21670b38(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"oxnske1cgaiylz0mwfv7p9r32h6qj8bt4d_u5"[i], 2) != 0) exit(1);
    i += 2;
}


__attribute__((constructor(112)))
void func_30b49da1(int argc, char **argv) {
    if (strncmp(&argv[1][i], &"3icj_go9qd0svxubefh14ktywpzma2l7nr685"[i], 2) != 0) exit(1);
    i += 2;
}


int main(int argc, char **argv) {
	puts("CONGRATULATIONS!");
    printf("The flag is ctf4b{%s}\n", argv[1]);
	_exit(0);
}

__attribute__((destructor))
void func_dc69ef50() {
	puts("WRONG");
}

