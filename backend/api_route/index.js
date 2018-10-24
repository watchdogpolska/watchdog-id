const Router = require("koa-router");


module.exports = () => {
    const router = new Router();

    for (const name of ['user', 'service']) {
        const subrouter = require(`./${name}`)();
        router.use(`/${name}`, subrouter.routes(), subrouter.allowedMethods())
    }

    return router;
}
