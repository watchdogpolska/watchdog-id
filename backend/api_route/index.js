'use strict';
const Router = require('koa-router');


const sections = [
    'user',
    'service',
    'access_request',
    'role',
    'oauth2',
    'client'
];

module.exports = () => {
    const router = new Router();

    for (const name of sections) {
        const subrouter = require(`./${name}`)();
        router.use(`/${name}`, subrouter.routes(), subrouter.allowedMethods());
    }

    return router;
};
