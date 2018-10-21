FROM node:10

WORKDIR /src
COPY package* ./
RUN npm ci
CMD nodejs index.js
