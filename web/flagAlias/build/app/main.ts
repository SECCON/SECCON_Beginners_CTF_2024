import * as flag from "./flag.ts";

function waf(key: string) {
  // Wonderful WAF :)
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
  for (const word of ngWords) {
    if (key.includes(word)) {
      return "'NG word detected'";
    }
  }
  return key;
}

export async function chall(alias = "`real fl${'a'.repeat(10)}g`") {
  const m: { [key: string]: string } = {
    "wonderful flag": "fake{wonderful_fake_flag}",
    "special flag": "fake{special_fake_flag}",
  };
  try {
    // you can set the flag alias as the key
    const key = await eval(waf(alias));
    m[key] = flag.getFakeFlag();
    return JSON.stringify(Object.entries(m), null, 2);
  } catch (e) {
    return e.toString();
  }
}

const handler = async (request: Request): Promise<Response> => {
  try {
    const body = JSON.parse(await request.text());
    const alias = body?.alias;
    return new Response(await chall(alias), { status: 200 });
  } catch (_) {
    return new Response('{"error": "Internal Server Error"}', { status: 500 });
  }
};

if(Deno.version.deno !== "1.42.0"){
  console.log("Please use deno 1.42.0");
  Deno.exit(1);
}
const port = Number(Deno.env.get("PORT")) || 3000;
Deno.serve({ port }, handler);
