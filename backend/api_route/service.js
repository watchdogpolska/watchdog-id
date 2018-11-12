'use strict';
const {createRouter} = require('../lib/resources');

const ServiceResource = {
    list: {},
    create: {
                req_schema: ctx => ({
            $async: true,
            type: 'object',
            properties: {
                title: {type: 'string'},
                description: {type: 'string'},
                status: {type: 'string', default: 'active'},
            },
            required: ['title', 'description', 'status'],
        }),
    },
    get: {},
    update: {},
    delete: {},
    subs: {
        Role: {
            list: {
                handler: model => async ctx => ctx.body = await model.find({serviceId: ctx.params.serviceId}),
            }
        }
    }
};

module.exports = () => createRouter('Service', ServiceResource);
