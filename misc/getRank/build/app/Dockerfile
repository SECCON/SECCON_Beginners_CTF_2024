FROM node:20-alpine3.19

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app
COPY main.ts package.json pnpm-lock.yaml /app
COPY public/ /app/public
RUN pnpm install

RUN adduser -D ctf4b
USER ctf4b

CMD ["pnpm", "run", "start"]