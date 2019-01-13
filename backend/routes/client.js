'use strict';
const {createService} = require('../lib/resources');

const Resource = () => ({
    schemas: {
        Client: {
            type: 'object',
            properties: {
                name: {
                    type: 'string',
                },
                redirect_uri: {
                    type: 'array',
                    items: {
                        type: 'string',
                    },
                },
                secret: {
                    type: 'string',
                },
            },
        },
    },
    list: {},
    create: {
        handler: model => async ctx => ctx.body = await model
            .create(ctx.request.body)
            .then(async doc => ({
                name: doc.name,
                redirect_uri: doc.redirect_uri,
                client_secret: await doc.client_secret,
                _id: doc._id,
            })),
    },
    get: {},
    update: {},
    delete: {},
});
module.exports = (basePath, options) => createService(basePath, 'Client', Resource, options);
