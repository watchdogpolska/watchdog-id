'use strict';
const model = require('./model');
const Koa = require("koa");
const Router = require("koa-router");
const BodyParser = require("koa-bodyparser");
const settings = require("./settings");
const mongoose = require('mongoose');


const http = require('http');

const main = (options) => new Promise(async (resolve, reject) => {
    const config = Object.assign({}, settings, process.env, options);

    const connection = await mongoose.connect(config.MONGODB_URL, {
        useCreateIndex: true,
        useNewUrlParser: true
    });
    await mongoose.model('User', model.userSchema);
    await mongoose.model('Role', model.roleSchema);
    await mongoose.model('AccessRequest', model.accessRequestSchema);
    await mongoose.model('Service', model.serviceSchema);
    const app = new Koa();
    app.use(BodyParser());

    const api_router = require('./api_route')(connection);

    const router = new Router()
        .all('/', (ctx) => ctx.body = ctx.request.body)
        .use('/v1', api_router.routes(), api_router.allowedMethods());

    app.use(router.routes(), router.allowedMethods());

    const server = http.createServer(app.callback());
    server.once('listening', () => resolve(server));
    server.once('error', reject);
    server.listen(config.LISTEN_PORT || 3000);
});

if (require.main === module) {
    main().catch(console.error);
}

module.exports = main;
