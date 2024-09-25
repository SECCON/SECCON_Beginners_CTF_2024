#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
  char buf[100];
  FILE *f = fopen("./flag.txt", "r");
  fgets(buf, 100, f);
  puts(buf);
}

int main() {
  char buf[10] = {0};
  printf("input:");
  read(0, buf, 0x20);
  printf("Hello, %s\n", buf);
  printf("return to: 0x%lx\n", *(uint64_t *)(((void *)buf) + 18));
  return 0;
}

__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(120);
}
