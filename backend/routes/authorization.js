'use strict';
const {createService} = require('../lib/resources');
const {notFound} = require('boom');

const Resource = () => ({
    schemas: {
        Authorization: {
            type: 'object',
            properties: {
                client: {
                    type: 'string',
                },
                scope: {
                    type: 'array',
                    items: {
                        type: 'string',
                        enum: Object.keys(require('./../model/scopes.js')),
                    },
                },
                redirect_uri: {
                    type: 'string',
                },
                user: {
                    type: 'string',
                },
                description: {
                    type: 'string',
                },
            },
        },
    },
    list: {},
    create: {
        security: [
            {
                basicAuth: [],
            },
            {
                apiKeyAuth: [],
            },
            {
                cookieAuth: [],
            },
        ],
        handler: model => async ctx => {
            const authorization = model({
                scope: ctx.request.body.scope,
                user: ctx.state.user._id,
            });
            await authorization.save();

            ctx.body = {
                authorization: authorization,
                access_token: await authorization.access_token,
                refresh_token: await authorization.refresh_token,
                token_type: 'Bearer',
                user: authorization.user,
            };
        },
    },
    get: {
        handler: model => async ctx => {
            ctx.body = await model.findOne({
                user: ctx.state.user._id,
                _id: ctx.params.id,
            });
        },
    },
    update: {},
    delete: {
        handler: model => async ctx => {
            const authorization = await model.findOne({
                user: ctx.state.user._id,
                _id: ctx.params.id,
            });
            if (!authorization) {
                return notFound('');
            }
            await authorization.remove();
            ctx.body = authorization;
        },
    },
});
module.exports = (basePath, options) => createService(basePath, 'Authorization', Resource, options);
