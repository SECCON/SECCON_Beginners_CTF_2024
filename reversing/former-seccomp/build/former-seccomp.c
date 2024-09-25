#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/fcntl.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/signal.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <syscall.h>
#include <unistd.h>

char enc_flag[] = {0xa5, 0xd2, 0xbc, 0x02, 0xb2, 0x7c, 0x86, 0x38, 0x17,
                   0xb1, 0x38, 0xc6, 0xe4, 0x5c, 0x1f, 0xa0, 0x9d, 0x96,
                   0xd1, 0xf0, 0x4b, 0xa6, 0xa6, 0x5c, 0x64, 0xb7, 0x00};

char enc_key[] = {0x43, 0x55, 0x44, 0x17, 0x46, 0x1f,
                  0x14, 0x17, 0x1a, 0x1d, 0x00};

void child() {
  if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
    printf("don't debug me!\n");
    exit(1);
  }
  if (kill(getpid(), SIGSTOP) == -1) {
    perror("kill");
    exit(1);
  }

  printf("flag> ");

  char buf[64], flag[64];
  fgets(buf, 64, stdin);
  if (sscanf(buf, "ctf4b{%26s%[}]", flag, buf) != 2) {
    printf("invalid format\n");
    exit(1);
  }

  int result = syscall(0xcafe, flag, strlen(flag));
  if (result) {
    puts("CONGRATULATIONS!");
  } else {
    puts("WRONG");
  }

  exit(0);
}

#define N 256

void swap(unsigned char *a, unsigned char *b) {
  char tmp = *a;
  *a = *b;
  *b = tmp;
}

char *rc4(char *text, char *key) {
  size_t text_len = strlen(text);
  char *ret = malloc(text_len);
  unsigned char s[N];

  int key_len = strlen(key);
  for (size_t i = 0; i < N; i++) {
    s[i] = i;
  }

  for (size_t i = 0, j = 0; i < N; i++) {
    j = (j + s[i] + key[i % key_len]) % N;
    swap(&s[i], &s[j]);
  }

  for (size_t i = 0, j = 0, n = 0; n < text_len; n++) {
    i = (i + 1) % N;
    j = (j + s[i]) % N;
    swap(&s[i], &s[j]);
    ret[n] = (s[(s[i] + s[j]) % N]) ^ text[n];
  }

  return ret;
}

int check_flag(char *buf) {
  size_t buf_len = strlen(buf);
  if (buf_len != sizeof(enc_flag) - 1) {
    return 0;
  }

  for (size_t i = 0; i < strlen(enc_key); i++) {
    enc_key[i] ^= (0x20 + i);
  }

  char *flag = rc4(enc_flag, enc_key);

  for (size_t i = 0; buf[i] && flag[i]; i++) {
    if (buf[i] != flag[i]) {
      return 0;
    }
  }

  return 1;
}

void parent(pid_t pid) {
  int status;

  waitpid(pid, &status, 0);
  if (!(WIFSTOPPED(status) && WSTOPSIG(status) == SIGSTOP))
    exit(1);

  ptrace(PTRACE_SETOPTIONS, pid, 0, PTRACE_O_EXITKILL);

  while (1) {
    // enter syscall
    if (ptrace(PTRACE_SYSCALL, pid, 0, 0) == -1) {
      perror("ptrace");
      exit(1);
    }
    if (waitpid(pid, &status, __WALL) == -1) {
      perror("waitpid");
      exit(1);
    }
    if (!(WIFSTOPPED(status) && WSTOPSIG(status) == SIGTRAP))
      break;

    struct user_regs_struct regs;
    if (ptrace(PTRACE_GETREGS, pid, 0, &regs) == -1) {
      perror("ptrace");
      exit(1);
    }

    if (regs.orig_rax == 0xcafe) {
      char buf[32] = {};
      unsigned long long read_bytes = 0;
      while (read_bytes < regs.rsi) {
        long tmp_buf = ptrace(PTRACE_PEEKDATA, pid, regs.rdi + read_bytes, 0);
        memcpy(buf + read_bytes, &tmp_buf, 1);
        read_bytes += 1;
      }
      buf[read_bytes] = '\0';

      regs.rax = check_flag(buf);
    }

    // exit syscall
    if (ptrace(PTRACE_SYSCALL, pid, 0, 0) == -1) {
      perror("ptrace");
      exit(1);
    }
    if (waitpid(pid, &status, __WALL) == -1) {
      perror("waitpid");
      exit(1);
    }
    if (!(WIFSTOPPED(status) && WSTOPSIG(status) == SIGTRAP))
      break;

    if (regs.orig_rax == 0xcafe) {
      if (ptrace(PTRACE_POKEUSER, pid, RAX * 8, regs.rax) == -1) {
        perror("ptrace");
        exit(1);
      }
    }
  }
}

int main() {
  pid_t pid = fork();
  if (pid == -1) {
    perror("fork");
    exit(1);
  }

  if (pid == 0) {
    child();
  } else {
    parent(pid);
  }
}
