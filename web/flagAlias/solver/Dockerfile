FROM denoland/deno:alpine

WORKDIR /app

ENV PATH="/root/.deno/bin:$PATH"

COPY . .

RUN adduser -D ctf4b
USER ctf4b

ENV HOST=0.0.0.0
ENV PORT=80

CMD ["deno", "task", "run"]