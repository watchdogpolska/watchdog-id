const Router = require("koa-router");
const mongoose = require('mongoose');

const {authenticatedOnly} = require('../lib/auth');

const toArray = value => Array.isArray(value) ? value : [value];

function getStack(spec, model, parents) {
    let stack = toArray(spec.handler(model, ...parents));
    if (!spec.unauthenticatedAccess) {
        stack = [authenticatedOnly, ...stack];
    }
    return stack;
}

const createRouter = (name, resource, options = {}) => {
    const router = new Router();
    const parents = options.parents || [];
    const model = mongoose.model(name);

    if (resource.list) {
        router.get("/", ...getStack(resource.list, model, parents))
    }

    if (resource.create) {
        router.post("/", ...getStack(resource.create, model, parents))
    }

    if (resource.get) {
        router.get("/:id",...getStack(resource.get, model, parents));
    }

    if (resource.delete) {
        router.del("/:id", ...getStack(resource.delete, model, parents));
    }

    for (const [subname, subresource] of Object.entries(resource.subs || {})) {
        const subrouter = createRouter(subname, subresource, {
            parents: [model, ...parents]
        });
        router.use(`/:${name.toLowerCase()}Id/${subname.toLowerCase()}`, subrouter.routes(), subrouter.allowedMethods());
    }
    return router;
};


module.exports = {
    createRouter
};
