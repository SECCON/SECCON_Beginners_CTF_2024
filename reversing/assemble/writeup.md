# assemble

1. Only mov, push, syscall instructions can be used.
2. The number of instructions should be less than 25.

これらの2つの条件を満たしながら、アセンブリコードを書いてみる問題となっています。

## Challenge 1. Please write 0x123 to RAX!

RAXレジスタに0x123を書き込むアセンブリコードを書きます。

RAXレジスタに値を書き込むには、mov命令を使います。今回はIntel構文を使っているので、mov命令の第一オペランドに書き込む先のレジスタ、第二オペランドに書き込む値を指定します。

```sh
mov  rax, 0x123
```

## Challenge 2. Please write 0x123 to RAX and push it on stack!

RAXレジスタに0x123を書き込み、その値をスタックにプッシュします。

RAXレジスタへの書き込みはChallenge 1で行ったものを使います。そして、RAXレジスタの値をスタックにプッシュするために、push命令を使います。

```sh
mov  rax, 0x123
push rax
```

## Challenge 3. Please use syscall to print Hello on stdout!

Helloを標準出力に出力するためのアセンブリコードを書きます。

システムコールを使うためには、syscall命令を使います。システムコール番号はRAXレジスタに、引数はRDI, RSI, RDXレジスタに格納します。

標準出力に出力するためには、システムコール番号1をRAXレジスタに格納し、引数として標準出力のファイルディスクリプタ1をRDIレジスタに格納します。そして、出力する文字列のアドレスをRSIレジスタに格納します。最後に、出力する文字列の長さをRDXレジスタに格納します。

出力する文字列は、Helloという文字列です。Helloという文字列はASCIIコードで表すと、0x48656c6c6fとなります。しかし、リトルエンディアンでデータが格納されるため、0x6f6c6c6548としてmov命令でRAXレジスタに格納します。そしてこの文字列をスタックにプッシュすることで、RSPレジスタに文字列のアドレスが格納されます。それをRSIレジスタに格納します。

そして、文字列の長さをRDXレジスタに格納します。Helloという文字列は5文字なので、5をRDXレジスタに格納します。

最後に、syscall命令を使ってシステムコールを実行します。これにより、Helloという文字列が標準出力に出力されます。

```sh
mov  rax, 0x6f6c6c6548
push rax
mov  rax, 1
mov  rdi, 1
mov  rsi, rsp
mov  rdx, 5
syscall
```

## Challenge 4. Please read flag.txt file and print it to stdout!

flag.txtファイルを読み込み、その内容を標準出力に出力するためのアセンブリコードを書きます。

まず、flag.txtファイルを開くために、sys_openシステムコールを使います。sys_openシステムコールのシステムコール番号は2です。引数として、ファイル名のアドレスをRDIレジスタに、ファイルのオープンモードをRSIレジスタに格納します。

次に、ファイルを読み込むために、sys_readシステムコールを使います。sys_readシステムコールのシステムコール番号は0です。引数として、ファイルディスクリプタをRDIレジスタに、読み込むバッファのアドレスをRSIレジスタに、読み込むバッファのサイズをRDXレジスタに格納します。

最後に、読み込んだファイルの内容を標準出力に出力するために、sys_writeシステムコールを使います。sys_writeシステムコールのシステムコール番号は1です。引数として、ファイルディスクリプタをRDIレジスタに、書き込むバッファのアドレスをRSIレジスタに、書き込むバッファのサイズをRDXレジスタに格納します。

これで、flag.txtファイルの内容が標準出力に出力されます。

```sh
mov  rax, 0                  # null terminate
push rax                     # push null to stack
mov  rax, 0x7478742e67616c66 # "flag.txt"
push rax                     # push file name to stack

mov  rdi, rsp  # file name buffer pointer
mov  rsi, 0    # O_RDONLY
mov  rax, 2    # syscall number

syscall        # sys_open

mov  rdi, rax  # fd
mov  rsi, rsp  # buffer pointer
mov  rdx, 1024 # buffer size
mov  rax, 0    # syscall number

syscall        # sys_read

mov  rdx, rax  # buffer size
mov  rsi, rsp  # buffer pointer
mov  rdi, 1    # stdout
mov  rax, 1    # syscall number

syscall        # sys_write
```
