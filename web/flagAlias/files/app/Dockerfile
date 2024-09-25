FROM denoland/deno:alpine-1.42.0

WORKDIR /app

ENV PATH="/root/.deno/bin:$PATH"

COPY . .

RUN adduser -D ctf4b
USER ctf4b

CMD ["deno", "task", "run"]