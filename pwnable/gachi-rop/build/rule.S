  A = arch
  A == ARCH_X86_64 ? next : dead
  A = sys_number
  A >= 0x40000000 ? dead : next
  A == execve ? dead : next
  A == execveat ? dead : next
  return ALLOW
dead:
  return ERRNO(0)