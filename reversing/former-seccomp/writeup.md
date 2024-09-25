# former-seccomp

`former-seccomp`という名前のプログラムが与えられる。
このプログラムを実行してみると、入力したフラグが正しいかどうかを判定してくれることがわかる。

```shell
$ ./former-seccomp 
flag> hoge 
invalid format
```

適当なデコンパイラ（このwriteupではGhidraを使用した）を用いて、プログラムを解析する。
問題のプログラムはstripされておりシンボル情報がないため、まずはmain関数を特定する必要がある。
そのためにentry関数の中で__libc_start_main関数を呼び出している箇所を探す。
ここで第1引数に渡されている`FUN_00101b80`がmain関数である。

```c
void processEntry entry(undefined8 param_1,undefined8 param_2)

{
  undefined auStack_8 [8];
  
  __libc_start_main(FUN_00101b80,param_2,&stack0x00000008,0,0,param_1,auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

`FUN_00101b80`をデコンパイルすると以下のようなコードが得られる。

```c
undefined8 FUN_00101b80(void)

{
  __pid_t _Var1;
  
  _Var1 = fork();
  if (_Var1 == -1) {
    perror("fork");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  if (_Var1 == 0) {
    // 子プロセスが実行する処理
    FUN_00101309();
  }
  else {
    // 親プロセスが実行する処理
    FUN_00101838(_Var1);
  }
  return 0;
}
```

`fork`を呼び出して新しいプロセスを生成し、親プロセスと子プロセスで処理を分岐していることがわかる。
まずは子プロセスの処理である`FUN_00101309`を調査する。

```c
void FUN_00101309(void)

{
  __pid_t __pid;
  int iVar1;
  long lVar2;
  size_t sVar3;
  long in_FS_OFFSET;
  char local_98 [64];
  char local_58 [72];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);

  // アンチデバッグ処理
  lVar2 = ptrace(PTRACE_TRACEME,0,0,0);
  if (lVar2 < 0) {
    puts("don\'t debug me!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  __pid = getpid();
  iVar1 = kill(__pid,0x13);
  if (iVar1 == -1) {
    perror("kill");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }

  // フラグの入力を受け付ける
  // フラグの形式はctf4b{}で、{}の中に26文字の文字列が入る
  printf("flag> ");
  fgets(local_98,0x40,stdin);
  iVar1 = __isoc99_sscanf(local_98,"ctf4b{%26s%[}]",local_58,local_98);
  if (iVar1 != 2) {
    puts("invalid format");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }

  // 0xcafeというシステムコールを呼び出して正誤判定を行う
  // 引数は、入力したフラグ文字列とその長さの2つ
  sVar3 = strlen(local_58);
  lVar2 = syscall(0xcafe,local_58,sVar3);
  // 0が返ってきた場合は不正解
  if ((int)lVar2 == 0) {
    puts("WRONG");
  }
  // 0以外が返ってきた場合は正解
  else {
    puts("CONGRATULATIONS!");
  }
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

この関数からは、主に2つのことがわかる。

1. フラグの形式は`ctf4b{26文字の文字列}`である
2. 0xcafeというシステムコールを呼び出して正誤判定を行っている

writeup執筆時点でシステムコール番号は最大で332までしか存在しないため、0xcafeはこのプログラムで何らかの方法でハンドルされるシステムコールであると考えられる。

次に親プロセスの処理である`FUN_00101838`を調査する。
わかりやすさのため、以下のコードでは`local_118`と`local_38`の変数の型をそれぞれ変更している。

```c
void FUN_00101838(uint param_1)

{
  __pid_t _Var1;
  int iVar2;
  long lVar3;
  long in_FS_OFFSET;
  uint local_12c;
  long local_128;
  ulong local_120;
  user_regs_struct local_118;
  char local_38 [32];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  waitpid(param_1,(int *)&local_12c,0);
  if (((local_12c & 0xff) != 0x7f) || ((local_12c & 0xff00) != 0x1300)) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  ptrace(PTRACE_SETOPTIONS,(ulong)param_1,0,0x100000);
  while( true ) {
    // ptraceを用いてシステムコールの呼び出しを監視する（システムコールに入るとき）
    lVar3 = ptrace(PTRACE_SYSCALL,(ulong)param_1,0,0);
    if (lVar3 == -1) {
      perror("ptrace");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    _Var1 = waitpid(param_1,(int *)&local_12c,0x40000000);
    if (_Var1 == -1) {
      perror("waitpid");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    if (((local_12c & 0xff) != 0x7f) || ((local_12c & 0xff00) != 0x500)) break;
    lVar3 = ptrace(PTRACE_GETREGS,(ulong)param_1,0,&local_118);
    if (lVar3 == -1) {
      perror("ptrace");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }

    // システムコール番号が0xcafeのとき
    if (local_118.orig_rax == 0xcafe) {
      // local_38にあるバッファを0で初期化
      local_38[0] = '\0';
      local_38[1] = '\0';
      local_38[2] = '\0';
      local_38[3] = '\0';
      local_38[4] = '\0';
      local_38[5] = '\0';
      local_38[6] = '\0';
      local_38[7] = '\0';
      local_38[8] = '\0';
      local_38[9] = '\0';
      local_38[10] = '\0';
      local_38[11] = '\0';
      local_38[12] = '\0';
      local_38[13] = '\0';
      local_38[14] = '\0';
      local_38[15] = '\0';
      local_38[16] = '\0';
      local_38[17] = '\0';
      local_38[18] = '\0';
      local_38[19] = '\0';
      local_38[20] = '\0';
      local_38[21] = '\0';
      local_38[22] = '\0';
      local_38[23] = '\0';
      local_38[24] = '\0';
      local_38[25] = '\0';
      local_38[26] = '\0';
      local_38[27] = '\0';
      local_38[28] = '\0';
      local_38[29] = '\0';
      local_38[30] = '\0';
      local_38[31] = '\0';
      // local_118.rsi（システムコールの引数に与えられたバッファ）とlocal_118.rdi（システムコールの引数に与えられたバッファの長さ）を参照して、local_38にデータをコピー
      for (local_120 = 0; local_120 < local_118.rsi; local_120 = local_120 + 1) {
        local_128 = ptrace(PTRACE_PEEKDATA,(ulong)param_1,local_118.rdi + local_120,0);
        local_38[local_120] = (char)local_128;
      }
      local_38[local_120] = '\0';
      // local_38にあるデータを引数にしてFUN_00101737を呼び出し、その返り値をlocal_118.raxに代入
      iVar2 = FUN_00101737(local_38);
      local_118.rax = (long)iVar2;
    }

    // ptraceを用いてシステムコールの呼び出しを監視する（システムコールから抜けるとき）
    lVar3 = ptrace(PTRACE_SYSCALL,(ulong)param_1,0,0);
    if (lVar3 == -1) {
      perror("ptrace");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    _Var1 = waitpid(param_1,(int *)&local_12c,0x40000000);
    if (_Var1 == -1) {
      perror("waitpid");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    if (((local_12c & 0xff) != 0x7f) || ((local_12c & 0xff00) != 0x500)) break;

    // システムコール番号が0xcafeのとき
    if (local_118.orig_rax == 0xcafe) {
      // システムコールの返り値をlocal_118.rax（FUN_00101737の返り値）の値に書き換える
      lVar3 = ptrace(PTRACE_POKEUSER,(ulong)param_1,0x50,local_118.rax);
      if (lVar3 == -1) {
        perror("ptrace");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

この関数からは、主に2つのことがわかる。

1. ptraceを用いてシステムコールの呼び出しを監視している
2. システムコール番号が0xcafeのとき、そのシステムコールの引数に与えられた文字列を取得し、その文字列を引数にして`FUN_00101737`を呼び出している
3. `FUN_00101737`の返り値をシステムコールの返り値としている

したがって、`FUN_00101737`を調査すればフラグの正誤判定のロジックがわかりそうである。
`FUN_00101737`をデコンパイルすると以下のようなコードが得られる。

```c
undefined8 FUN_00101737(char *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  long lVar3;
  ulong local_28;
  long local_20;
  
  sVar1 = strlen(param_1);
  // 引数param_1の文字列が26文字であるかどうかを確認
  if (sVar1 == 0x1a) {
    // グローバル変数DAT_00104030にある文字列に対してXORを取る
    for (local_28 = 0; sVar1 = strlen(&DAT_00104030), local_28 < sVar1; local_28 = local_28 + 1) {
      (&DAT_00104030)[local_28] = (char)local_28 + 0x20U ^ (&DAT_00104030)[local_28];
    }
    // グローバル変数DAT_00104010とグローバル変数DAT_00104030を引数にしてFUN_00101497を呼び出し、その返り値をローカル変数lVar3に代入
    lVar3 = FUN_00101497(&DAT_00104010,&DAT_00104030);
    // 引数param_1と、ローカル変数lVar3にある文字列が一致しているかどうかを確認
    for (local_20 = 0; (param_1[local_20] != '\0' && (*(char *)(local_20 + lVar3) != '\0'));
        local_20 = local_20 + 1) {
      if (param_1[local_20] != *(char *)(local_20 + lVar3)) {
        return 0;
      }
    }
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}
```

ここで、引数の文字列とFUN_00101497の返り値から得られる文字列が等しいかを確認している処理が見つかった。
この引数の文字列は入力したフラグであるから、変数lVar3の中身を調査すれば正しいフラグがわかると考えられる。

そこで、デバッガを用いて変数lVar3の中身を調査する。

```shell
$ gdb ./former-seccomp 
[snip]
pwndbg> set follow-fork-mode parent
pwndbg> r
[snip]
flag> ^C
pwndbg> brva 0x17d3
pwndbg> r
[snip]
flag> ctf4b{aaaaaaaaaaaaaaaaaaaaaaaaaa}

Breakpoint 1, 0x00005555555557d3 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
──────────────────────────────────────────────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]───────────────────────────────────────────────────────────────────────────────────────────
*RAX  0x5555555592a0 ◂— 'p7r4c3_c4n_3mul4t3_sysc4ll'
*RBX  0x7fffffffda08 —▸ 0x7fffffffdce4 ◂— '/home/user01/src/github.com/SECCON/2024_beginnersctf_ctf/reversing/former-seccomp/files/former-seccomp'
*RCX  0xb7
 RDX  0
*RDI  0x7fffffffd63a ◂— 0xa03c92f8c5227187
*RSI  0x6c
*R8   0x7ffff7e03b20 (main_arena+96) —▸ 0x5555555592c0 ◂— 0
*R9   0x30
*R10  1
 R11  0
*R12  1
 R13  0
*R14  0x555555557d50 —▸ 0x5555555552c0 ◂— endbr64 
*R15  0x7ffff7ffd000 (_rtld_global) —▸ 0x7ffff7ffe2e0 —▸ 0x555555554000 ◂— 0x10102464c457f
*RBP  0x7fffffffd770 —▸ 0x7fffffffd8c0 —▸ 0x7fffffffd8e0 —▸ 0x7fffffffd980 —▸ 0x7fffffffd9e0 ◂— ...
*RSP  0x7fffffffd740 ◂— 0
*RIP  0x5555555557d3 ◂— mov qword ptr [rbp - 8], rax
───────────────────────────────────────────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────────────────────────────────────────────────────────────────
 ► 0x5555555557d3    mov    qword ptr [rbp - 8], rax      [0x7fffffffd768] => 0x5555555592a0 ◂— 'p7r4c3_c4n_3mul4t3_sysc4ll'
   0x5555555557d7    mov    qword ptr [rbp - 0x18], 0     [0x7fffffffd758] => 0
   0x5555555557df    jmp    0x55555555580d              <0x55555555580d>
    ↓
   0x55555555580d    mov    rdx, qword ptr [rbp - 0x28]     RDX, [0x7fffffffd748] => 0x7fffffffd890 ◂— 'aaaaaaaaaaaaaaaaaaaaaaaaaa'
   0x555555555811    mov    rax, qword ptr [rbp - 0x18]     RAX, [0x7fffffffd758] => 0
   0x555555555815    add    rax, rdx                        RAX => 0x7fffffffd890 (0x0 + 0x7fffffffd890)
   0x555555555818    movzx  eax, byte ptr [rax]             EAX, [0x7fffffffd890] => 0x61
   0x55555555581b    test   al, al                          0x61 & 0x61     EFLAGS => 0x202 [ cf pf af zf sf IF df of ]
   0x55555555581d    je     0x555555555831              <0x555555555831>
 
   0x55555555581f    mov    rdx, qword ptr [rbp - 8]        RDX, [0x7fffffffd768] => 0x5555555592a0 ◂— 'p7r4c3_c4n_3mul4t3_sysc4ll'
   0x555555555823    mov    rax, qword ptr [rbp - 0x18]     RAX, [0x7fffffffd758] => 0
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffd740 ◂— 0
01:0008│-028 0x7fffffffd748 —▸ 0x7fffffffd890 ◂— 'aaaaaaaaaaaaaaaaaaaaaaaaaa'
02:0010│-020 0x7fffffffd750 ◂— 0xa /* '\n' */
03:0018│-018 0x7fffffffd758 ◂— 0
04:0020│-010 0x7fffffffd760 ◂— 0x1a
05:0028│-008 0x7fffffffd768 ◂— 0
06:0030│ rbp 0x7fffffffd770 —▸ 0x7fffffffd8c0 —▸ 0x7fffffffd8e0 —▸ 0x7fffffffd980 —▸ 0x7fffffffd9e0 ◂— ...
07:0038│+008 0x7fffffffd778 —▸ 0x555555555a6a ◂— cdqe 
───────────────────────────────────────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ► 0   0x5555555557d3
   1   0x555555555a6a
   2   0x555555555bcf
   3   0x7ffff7c2a1ca __libc_start_call_main+122
   4   0x7ffff7c2a28b __libc_start_main+139
   5   0x555555555245
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> 
```

ここで、RAXレジスタの値を見ると、`p7r4c3_c4n_3mul4t3_sysc4ll`という文字列が得られる。
したがって、正しいフラグは`ctf4b{p7r4c3_c4n_3mul4t3_sysc4ll}`である。
