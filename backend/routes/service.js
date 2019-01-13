'use strict';
const {createService} = require('../lib/resources');

const RoleResource = () => ({
    list: {
        handler: model => async ctx => ctx.body = await model.find({serviceId: ctx.params.serviceId}),
    },
});

const ServiceResource = () => ({
    schemas: {
        Service: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                title: {
                    type: 'string',
                },
                description: {
                    type: 'string',
                },
                endpointUrl: {
                    type: 'string',
                },
                features: {
                    type: 'object',
                    properties: {
                        passwordReset: {
                            type: 'boolean',
                        },
                        userProvidedUsername: {
                            type: 'boolean',
                        },
                    },
                },
                status: {
                    type: 'string',
                    enum: [
                        'pending',
                        'active',
                        'suspended',
                        'archived',
                    ],
                },
                active: {
                    description: 'If status == active',
                    type: 'boolean',
                    readOnly: true,
                },
                createdBy: {
                    type: 'string',
                    readOnly: true,
                },
                createdAt: {
                    type: 'string',
                    readOnly: true,
                },
                modifiedBy: {
                    type: 'string',
                    readOnly: true,
                },
                modifiedAt: {
                    type: 'string',
                    readOnly: true,
                },
            },
        },
    },
    list: {},
    create: {
        // req_schema: ctx => ({
        //     $async: true,
        //     type: 'object',
        //     properties: {
        //         title: {type: 'string'},
        //         description: {type: 'string'},
        //         status: {type: 'string', default: 'active'},
        //     },
        //     required: ['title', 'description', 'status'],
        // }),
    },
    get: {},
    update: {},
    delete: {},
    subs: {
        Role: RoleResource,
    },
});
module.exports = (basePath, options) => createService(basePath, 'Service', ServiceResource, options);
