'use strict';
const {setUserMiddleware} = require('./lib/auth');

const model = require('./model');
const Koa = require('koa');
const Router = require('koa-router');
const BodyParser = require('koa-bodyparser');
const settings = require('./settings');
const signals = require('./signals');
// const mail = require('./mail');
const logger = require('koa-logger');
const mongoose = require('mongoose');
const boom_koa = require('./lib/boom_koa_middleware');
const http = require('http');

const main = (options) => new Promise(async (resolve, reject) => {
    const config = Object.assign({}, settings, process.env, options);

    await mongoose.connect(config.MONGODB_URL, {
        useCreateIndex: true,
        useNewUrlParser: true,
        useFindAndModify: false,
    });

    await require('./model').register();

    // mail.connect(signals);

    const app = new Koa();
    app.use(BodyParser());
    app.use(logger());
    app.use(setUserMiddleware());
    app.use(boom_koa());
    const api_router = require('./api_route')();
    const router = new Router();

    router.all('/', (ctx) => ctx.body = ctx.request.body);
    router.use('/v1', api_router.routes(), api_router.allowedMethods());

    // console.dir(router, {depth: null});
    // console.dir(api_router, {depth:null});
    app.use(router.routes());
    app.use(router.allowedMethods());

    const server = http.createServer(app.callback());

    server.once('listening', () => resolve(server));
    server.once('error', reject);
    server.listen(config.LISTEN_PORT || 3000);
});

if (require.main === module) {
    main()
        .then(() => console.log('Started server'))
        .catch(console.error);
}

module.exports = main;
