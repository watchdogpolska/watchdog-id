'use strict';
const Router = require('koa-router');
const mongoose = require('mongoose');
const {notFound} = require('boom');

const {authenticatedOnly} = require('../lib/auth');
const {req_schema_validator, res_schema_validator} = require('./schema.js');

const toArray = value => Array.isArray(value) ? value : [value];

function getStack(options) {
    const handler = options.handler || options.defaultHandler;
    const parents = options.parents || [];
    const model = options.model;
    const requireAuthentication = !options.unauthenticatedAccess;
    let stack = toArray(handler(model, ...parents));
    stack = [req_schema_validator, res_schema_validator, ...stack];


    if (requireAuthentication) {
        stack = [authenticatedOnly, ...stack];
    }

    if (options.req_schema) {
        const schema_handler = async (ctx, next) => {
            ctx.req_schema = await options.req_schema(ctx);
            return next();
        };
        stack = [schema_handler, ...stack];
    }

    if (options.res_schema) {
        const schema_handler = async (ctx, next) => {
            ctx.res_schema = await options.res_schema(ctx);
            return next();
        };
        stack = [schema_handler, ...stack];
    }

    return stack;
}

const actions = {
    list: {
        handler: model => async ctx => ctx.body = await model.find(),
        path: '/',
        method: 'get',
    },
    create: {
        handler: model => async ctx => ctx.body = await model.create(ctx.request.body),
        // req_schema: (ctx) => { ... },
        path: '/',
        method: 'post',
    },
    get: {
        handler: model => async ctx => {
            ctx.entry = await model.findOne({_id: ctx.params.id});
            if (!ctx.entry) {
                throw notFound('Unable to found entry');
            }
            ctx.body = ctx.entry.toJSON({virtuals: true});
        },
        path: '/:id',
        method: 'get',
    },
    update: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, ctx.request.body, {new: true}),
        path: '/:id',
        method: 'post',
    },
    delete: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, {status: 'suspended'}, {new: true}),
        path: '/:id',
        method: 'delete',
    },
};

const createRouter = (name, resource, options = {}) => {
    const router = new Router();

    const parents = options.parents || [];
    const model = mongoose.model(name);

    Object
        .entries(actions)
        .filter(([action_name]) => resource[action_name] !== undefined)
        .forEach(([action_name, param]) => router[param.method](
            param.path,
            ...getStack(Object.assign({}, param, options, resource[action_name], {
                model: model,
            }))
        ));

    Object
        .entries(resource.subs || {})
        .forEach(([subname, subresource]) => {
            const subrouter = createRouter(subname, subresource, {
                parents: [model, ...parents],
            });
            router.use(
                `/:${name.toLowerCase()}Id/${subname.toLowerCase()}`,
                subrouter.routes(),
                subrouter.allowedMethods()
            );
        });
    //
    // Object
    //     .entries(resource.actions || {})
    //     .forEach(([action_name, param]) =>
    //         router[param.method](`/action/:${action_name.toLowerCase()}`, param.handler)
    //     );

    return router;
};


module.exports = {
    createRouter,
};
