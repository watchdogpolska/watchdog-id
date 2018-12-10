'use strict';
const {createRouter} = require('../lib/resources');

const Resource = {
    list: {},
    create: {
        req_schema: () => ({
            $async: true,
            type: 'object',
            properties: {
                name: {type: 'string'},
                redirect_uri: {
                    type: "array", items: {
                        type: "string"
                    }
                }
            },
            required: ['name', 'redirect_uri'],
        }),
        handler: model => async ctx => ctx.body = await model
            .create(ctx.request.body)
            .then(async doc => ({
                name: doc.name,
                redirect_uri: doc.redirect_uri,
                client_secret: await doc.client_secret,
                _id: doc._id
            })),
    },
    get: {},
    update: {},
    delete: {},
};

module.exports = () => createRouter('Client', Resource);
