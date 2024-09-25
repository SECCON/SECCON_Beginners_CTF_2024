const PORT = Deno.env.get("PORT") || "80";
const HOST = Deno.env.get("HOST") || "localhost";

async function request(payload: string) {
  return await fetch(`http://${HOST}:${PORT}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ input: payload }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data;
    });
}

const payloads = [
  "0XF",
  "12.03",
  `1${"0".repeat(255)}`,
  `1${"0".repeat(256)}`,
  `1${"0".repeat(299)}`,
  `1${"0".repeat(300)}`,
  `0X${"F".repeat(256)}`, // valid payload
  `1${"0".repeat(309)}`,
];

payloads.forEach(async (payload) => {
  const res = await request(payload);
  console.log(`Payload: ${payload}\nResponse: ${JSON.stringify(res)}\n`);
});
