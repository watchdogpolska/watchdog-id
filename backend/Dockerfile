FROM node:10

WORKDIR /src
COPY package* ./
RUN npm install --production
COPY ./ ./
CMD nodejs index.js
