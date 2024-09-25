FROM node:21-alpine

WORKDIR /app

COPY package.json ./

RUN npm i

COPY . .

RUN adduser -D wooorker2
USER wooorker2

CMD ["npm", "start"]