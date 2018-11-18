FROM node:alpine
WORKDIR /opt/src
COPY ./package*.json ./
RUN npm install --only=production
COPY ./ ./
CMD ["npm", "run", "start"]
