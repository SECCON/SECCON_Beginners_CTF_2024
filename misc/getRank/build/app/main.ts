import fastify, { FastifyRequest } from "fastify";
import fs from "fs";

const RANKING = [10 ** 255, 1000, 100, 10, 1, 0];

type Res = {
  rank: number;
  message: string;
};

function ranking(score: number): Res {
  const getRank = (score: number) => {
    const rank = RANKING.findIndex((r) => score > r);
    return rank === -1 ? RANKING.length + 1 : rank + 1;
  };

  const rank = getRank(score);
  if (rank === 1) {
    return {
      rank,
      message: process.env.FLAG || "fake{fake_flag}",
    };
  } else {
    return {
      rank,
      message: `You got rank ${rank}!`,
    };
  }
}

function chall(input: string): Res {
  if (input.length > 300) {
    return {
      rank: -1,
      message: "Input too long",
    };
  }

  let score = parseInt(input);
  if (isNaN(score)) {
    return {
      rank: -1,
      message: "Invalid score",
    };
  }
  if (score > 10 ** 255) {
    // hmm...your score is too big?
    // you need a handicap!
    for (let i = 0; i < 100; i++) {
      score = Math.floor(score / 10);
    }
  }

  return ranking(score);
}

const server = fastify();

server.get("/", (_, res) => {
  res.type("text/html").send(fs.readFileSync("public/index.html"));
});

server.post(
  "/",
  async (req: FastifyRequest<{ Body: { input: string } }>, res) => {
    const { input } = req.body;
    const result = chall(input);
    res.type("application/json").send(result);
  }
);

server.listen(
  { host: "0.0.0.0", port: Number(process.env.PORT ?? 3000) },
  (err, address) => {
    if (err) {
      console.error(err);
      process.exit(1);
    }
    console.log(`Server listening at ${address}`);
  }
);
