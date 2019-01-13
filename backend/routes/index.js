'use strict';
const openapi_router = require('./../lib/openapi-router');
const Router = require('koa-router');

const sections = [
    'user',
    'service',
    'access_request',
    'role',
    'oauth2',
    'client',
    'authorization',
];

const router = new Router();
const swagger = openapi_router({
    router: router,
    info: require('./../package.json'),
    swaggerUiPath: process.env.NODE_ENV !== 'PRODUCTION' ? '/swagger' : false,
    redocUiPath: process.env.NODE_ENV !== 'PRODUCTION' ? '/redoc' : false,
});

for (const name of sections) {
    require(`./services/${name}`)(`/v1/${name}`, swagger);
}

module.exports = router;
