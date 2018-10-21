const Router = require("koa-router");

module.exports = connection => {
    const user_rouer = require('./user')(connection);
    return new Router()
        .use('/user', user_rouer.routes(), user_rouer.allowedMethods());
};
