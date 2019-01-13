'use strict';
const {createService} = require('../../lib/resources');
const getResource = () => ({
    schemas: {
        User: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                username: {
                    type: 'string',
                },
                first_name: {
                    type: 'string',
                },
                second_name: {
                    type: 'string',
                },
                email: {
                    type: 'string',
                },
                password: {
                    type: 'string',
                    writeOnly: true,
                },
                status: {
                    type: 'string',
                    enum: [
                        'pending',
                        'accepted',
                        'admin',
                        'suspended',
                    ],
                },
                active: {
                    description: 'If status == active',
                    type: 'boolean',
                    readOnly: true,
                },
            },
        },
    },
    list: {},
    create: {},
    get: {
        handler: model => async ctx => ctx.body = await model.findOne({_id: ctx.params.id === 'me' ? ctx.state.user._id : ctx.params.id}),
    },
    delete: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, {status: 'suspended'}, {new: true}),
    },
    subs: {
        Session: require('./session'),
        Factor: require('./factory'),
    },
});
module.exports = (basePath, swagger) => createService(basePath, 'User', getResource, swagger);
