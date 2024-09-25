# construct

`construct`という名前のプログラムが与えられる。
実行してみると、引数にパスワードをとり、そのパスワードが正しいかどうかを判定するプログラムであることがわかる。

```shell
$ ./construct 
usage: construct <password>
$ ./construct hoge
WRONG
```

Ghidraを用いてプログラムを解析する。
まず、main関数から調べる。

```c
void main(undefined8 param_1,long param_2)

{
  puts("CONGRATULATIONS!");
  // 引数に与えられたパスワードをフラグとして表示する
  printf("The flag is ctf4b{%s}\n",*(undefined8 *)(param_2 + 8));
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

プログラムの実行時に引数として与えられたパスワードをフラグとして表示することがわかる。
一見このようなプログラムでは常にCONGRATULATIONS!と表示されそうだが、実際にはそうではなかった。

そこで、WRONGを表示する処理を調べる。
GhidraのDefined Strings viewからWRONGという文字列を探し、その参照元を調べる。
すると以下の`func_dc69ef50`関数が見つかる。

```c
void func_dc69ef50(void)

{
  puts("WRONG");
  return;
}
```

このプログラムがどこから呼ばれているかを調べるために`func_dc69ef50`の参照元を確認すると、.fini_arrayというセクションから参照されていることがわかる。
.fini_arrayセクションはプログラムの終了時に実行される関数のアドレスが格納されているセクションである。
したがって、プログラムの終了時に`func_dc69ef50`関数が呼び出され、WRONGが表示されることがわかる。

```
                             //
                             // .fini_array 
                             // SHT_FINI_ARRAY  [0x3d90 - 0x3d9f]
                             // ram:00103d90-ram:00103d9f
                             //
                             __DT_FINI_ARRAY                                 XREF[2]:     00103df8(*), 
                             __do_global_dtors_aux_fini_array_entry                       _elfSectionHeaders::00000590(*)  
        00103d90 a0 11 10        addr       __do_global_dtors_aux
                 00 00 00 
                 00 00
        00103d98 65 19 10        addr       func_dc69ef50
                 00 00 00 
                 00 00
```

同様に、.init_arrayセクションについても確認してみる。このセクションはプログラムの開始時に実行される関数のアドレスが格納されているセクションである。
こちらも以下のようにいくつかの関数が登録されていることがわかる。
上から順にそれぞれの関数を調査する。

```
                             //
                             // .init_array 
                             // SHT_INIT_ARRAY  [0x3cf8 - 0x3d8f]
                             // ram:00103cf8-ram:00103d8f
                             //
                             __DT_INIT_ARRAY                                 XREF[4]:     00100168(*), 001002f0(*), 
                                                                                          00103dd8(*), 
                                                                                          _elfSectionHeaders::00000550(*)  
        00103cf8 e9 11 10        addr       func_e0db2736
                 00 00 00 
                 00 00
        00103d00 1e 12 10        addr       func_f8db6e92
                 00 00 00 
                 00 00
        00103d08 fb 16 10        addr       func_9e81c732
                 00 00 00 
                 00 00
        00103d10 8f 16 10        addr       func_2b08a7d1
                 00 00 00 
                 00 00
[snip]
```

まず1つめの`func_e0db2736`関数では、プログラム実行時の引数の数を確認して引数が1個でない場合にはusageを表示して終了している。

```c
void func_e0db2736(int param_1)

{
  if (param_1 != 2) {
    puts("usage: construct <password>");
                    /* WARNING: Subroutine does not return */
    _exit(1);
  }
  return;
}
```

2つめの`func_f8db6e92`関数では、引数に与えられた文字列の長さを確認して0x20文字でない場合には`exit`関数を呼び出している。

```c
void func_f8db6e92(undefined8 param_1,long param_2)

{
  size_t sVar1;
  
  sVar1 = strlen(*(char **)(param_2 + 8));
  if (sVar1 != 0x20) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  return;
}
```

3つめの`func_9e81c732`関数では、引数に与えられた文字列と定数の文字列の先頭の2文字が等しいかを確認し、等しくない場合には`exit`関数を呼び出している。

```c
void func_9e81c732(undefined8 param_1,long param_2)

{
  int iVar1;
  
  iVar1 = strncmp((char *)((long)i + *(long *)(param_2 + 8)),
                  "c096dv43ljgtzksyo_an8r57qmxwfeupb1ih2" + i,2);
  if (iVar1 != 0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  i = i + 2;
  return;
}
```

4つめ以降の関数については3つめの関数と同様であるため省略する。

ここまでにわかったことをまとめると、以下のようになる。

- プログラムの実行時の引数として、1つ引数が与えられていることを確認する
- 引数として与えられた文字列の長さが0x20であることを確認する
- 引数の文字列を先頭から2文字ずつ`strncmp`関数を用いて比較し、バイナリ内の定数と等しいことを確認する

つまり、`strncmp`関数に与えられた定数の文字列を観測できれば正しいパスワードが入手できそうである。
そのために、ltraceというコマンドを利用できる。
このコマンドは、プロセスが呼び出したライブラリ関数をトレースすることができる。

試しに、適当な0x20文字の文字列を与えてltraceコマンドでプログラムを実行してみる。

```shell
$ ltrace ./construct aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
strlen("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"...)                         = 32
strncmp("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"..., "c096dv43ljgtzksyo_an8r57qmxwfeup"..., 2) = -2
exit(1 <unfinished ...>
puts("WRONG"WRONG
)                                                         = 6
+++ exited (status 1) +++
```

文字列`"c096dv43ljgtzksyo_an8r57qmxwfeup"`と比較しており、この先頭2文字が正しいパスワードである。
引数の先頭を`"c0"`に変えて再度実行する。

```shell
$ ltrace ./construct  c0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
strlen("c0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"...)                         = 32
strncmp("c0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"..., "c096dv43ljgtzksyo_an8r57qmxwfeup"..., 2) = 0
strncmp("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "nswvxkgaoj08mp749tc56bqu1d32ehzf"..., 2) = -13
exit(1 <unfinished ...>
puts("WRONG"WRONG
)                                                         = 6
+++ exited (status 1) +++
```

`strncmp`が2回呼び出されるようになり、パスワードの次の2文字がわかった。
以上の動作を繰り返すことによって、パスワード全体を得ることができる。

```shell
$ ./construct c0ns7ruc70rs_3as3_h1d1ng_7h1ngs!
CONGRATULATIONS!
The flag is ctf4b{c0ns7ruc70rs_3as3_h1d1ng_7h1ngs!}
```

正しいパスワードを渡してプログラムを実行すると、フラグが得られた。
