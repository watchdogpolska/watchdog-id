'use strict';
const {createRouter} = require('../lib/resources');
const mongoose = require('mongoose');

const RoleResource = {
    list: {},
    create: {
        req_schema: ctx => ({
            $async: true,
            type: 'object',
            properties: {
                title: {type: 'string'},
                description: {type: 'string'},
                status: {type: 'string', default: 'active'},
                manager: {type: 'string', default: ctx.state.user._id},
                serviceId: {type: 'string'}
            },
            required: ['title', 'description', 'manager'],
        }),
        handler: (model) => async ctx => {
            const role = new model(ctx.request.body);
            await role.save();
            ctx.body = role;
        },
    },
    get: {},
    update: {},
    delete: {},
};

module.exports = () => createRouter('Role', RoleResource);
