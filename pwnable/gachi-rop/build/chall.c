#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>

static void install_seccomp() {
    static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,5,62,0,0,192,32,0,0,0,0,0,0,0,53,0,3,0,0,0,0,64,21,0,2,0,59,0,0,0,21,0,1,0,66,1,0,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,5,0};
    struct prog {
        unsigned short len;
        unsigned char *filter;
    } rule = {
        .len = sizeof(filter) >> 3,
        .filter = filter
    };
    if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
    if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) { perror("prctl(PR_SET_SECCOMP)"); exit(2); }
}

int main() {
    install_seccomp();
    printf("system@%p\n", (void *)system);
    char buf[0x10] = {0};
    printf("Name: ");
    gets(buf);
    printf("Hello, gachi-rop-%s!!\n", buf);
    return 0;
}

__attribute__((constructor)) void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(120);
}