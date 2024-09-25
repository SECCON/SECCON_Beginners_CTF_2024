# clamre

## 問題文
アンチウィルスのシグネチャを読んだことはありますか?

※サーバにアクセスしなくても解けます

[https://clamre.beginners.seccon.games](https://clamre.beginners.seccon.games)

## 難易度
**easy**

## 作問にあたって
clamavのシグネチャの読み方とPCREの読み方を理解して欲しい

## 解法
ファイルを見ると`clamscan`で`--database=/app/flag.ldb`を指定している。

配布ファイルの中にある`flag.ldb`を見ると正規表現があるので、これを気合で読むとマッチする文字列が特定できる。

キャプチャとHexの組み合わせなのでそこまで難しくはない。

`ctf4b{Br34k1ng_4ll_Th3_H0u53_Rul35}`
