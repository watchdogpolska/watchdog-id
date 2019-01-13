'use strict';
const {createService} = require('../lib/resources');

const RoleResource = () => ({
    schemas: {
        Role: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
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
                serviceId: {
                    type: 'integer',
                },
                name: {
                    type: 'string',
                },
                description: {
                    type: 'string',
                },
                active: {
                    description: 'If status == active',
                    type: 'boolean',
                },
                manager: {
                    type: 'string',
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
        handler: (model) => async ctx => {
            const role = new model(Object.assign({manager: ctx.state.user._id}, ctx.request.body));
            await role.save();
            ctx.body = role;
        },
    },
    get: {},
    update: {},
    delete: {},
});

module.exports = (basePath, options) => createService(basePath, 'Role', RoleResource, options);
