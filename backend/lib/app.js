const Koa = require('koa');

const BodyParser = require('koa-bodyparser');
const logger = require('koa-logger');
const boom_koa = require('./boom_koa_middleware');
const router = require('../routes');
const app = new Koa();

app.use(BodyParser());
app.use(logger());
app.use(boom_koa());
app.use(router.routes());
app.use(router.allowedMethods());

module.exports = app;
