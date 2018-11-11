'use strict';
const Router = require('koa-router');


module.exports = () => {
    const router = new Router();

    for (const name of ['user', 'service', 'access_request', 'role']) {
        const subrouter = require(`./${name}`)();
        router.use(`/${name}`, subrouter.routes(), subrouter.allowedMethods());
    }

    return router;
};
