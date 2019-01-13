'use strict';
const {createService} = require('../lib/resources');
const mongoose = require('mongoose');
const {badRequest, forbidden} = require('boom');
const signals = require('../lib/signals');

const OpinionResource = () => ({
    schemas: {
        Opinion: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                userId: {
                    type: 'string',
                    readOnly: true,
                },
                status: {
                    type: 'string',
                    enum: [
                        'accepted',
                        'rejected',
                        'pending',
                    ],
                },
                comment: {
                    type: 'string',
                },
            },
        },
    },
    list: {
        handler: (model, parent_model) => async ctx => {
            const service = await parent_model.findOne({_id: ctx.params.accessrequestId});
            ctx.body = service.opinions;
        },
    },
    // create: {},
    get: {
        handler: (model, parent_model) => async ctx => {
            const parent = await parent_model.findOne({
                _id: ctx.params.accessRequestId,
                'opinions._id': ctx.params.id,
            });
            ctx.body = parent.opinions.id(ctx.params.id);
        },
    },
    update: {
        handler: (model, parent_model) => async ctx => {
            const parent = await parent_model.findOne({
                _id: ctx.params.accessRequestId,
                'opinions._id': ctx.params.id,
            });
            const opinion = parent.opinions.id(ctx.params.id);

            if (opinion.userId.toString() !== ctx.state.user._id.toString() && !ctx.state.user.perms.includes('change_any_opinion')) {
                throw forbidden('You can only modify your own opinions.');
            }
            for (const status of ['accepted', 'rejected']) {
                if (ctx.request.body.status === status && opinion.status !== status) {
                    parent.events.push({
                        status: status,
                        finished: Date.now(),
                    });
                }
            }
            if (ctx.request.body.status === 'accepted' && opinion.status === 'pending') {
                if (!parent.opinions.find(x => x.status !== 'accepted' && x._id !== opinion._id)) {
                    parent.events.push({
                        status: 'queued',
                    });
                }
            }
            opinion.status = ctx.request.body.status;
            await parent.save();
            ctx.body = opinion;
        },
    },
    // delete: {},
});

const can_create_access_request = (user, body) => {
    if (user.perms.includes('create_own_access_request') && [user._id] === body.usersId) {
        return true;
    }
    if (user.perms.includes('create_any_access_request')) {
        return true;
    }
    return true;
};

const AccessRequestResource = () => ({
    schemas: {
        Event: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                accessRequestId: {
                    type: 'integer',
                },
                type: {
                    type: 'string',
                    enum: [
                        'created',
                        'accepted',
                        'rejected',
                        'queued',
                        'done',
                        'error',
                    ],
                },
                createdAt: {
                    type: 'string',
                    readOnly: true,
                },
                data: {
                    type: 'object',
                    additionalProperties: {
                        type: 'string',
                    },
                },
            },
        },
        AccessRequest: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                comment: {
                    type: 'string',
                },
                opinions: {
                    type: 'array',
                    readOnly: true,
                    items: {
                        $ref: '#/components/schemas/Opinion',
                    },
                },
                events: {
                    type: 'array',
                    readOnly: true,
                    items: {
                        $ref: '#/components/schemas/Event',
                    },
                },
                status: {
                    type: 'string',
                    enum: [
                        'pending',
                        'rejected',
                        'accepted',
                        'queued',
                        'done',
                        'error',
                    ],
                },
                usersId: {
                    type: 'array',
                    items: {
                        type: 'string',
                    },
                },
                rolesId: {
                    type: 'array',
                    items: {
                        type: 'string',
                    },
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
    list: {
        handler: model => async ctx => {
            let query = {};
            if (ctx.request.query.accessUserId) {
                query = Object.assign({}, query, {usersId: {$in: ctx.query.accessUserId}});
            }
            if (ctx.request.query.roleId) {
                query = Object.assign({}, query, {rolesId: {$in: ctx.query.roleId}});
            }
            if (ctx.request.query.opinionUserId) {
                query = Object.assign({}, query, {'opinions.userId': {$eq: ctx.query.opinionUserId}});
            }
            ctx.body = await model.find(query);
        },
    },
    create: {
        handler: (model) => async ctx => {
            if (!ctx.request.body) {
                throw badRequest('No authentication details have been provided.');
            }
            if (!can_create_access_request(ctx.state.user, ctx.request.body)) {
                throw forbidden('No sufficient permission to perform action');
            }
            const obj = model(ctx.request.body);
            obj.events.push({
                createdBy: ctx.state.user._id,
                status: 'created',
                finishedAt: Date.now(),
            });
            const User = mongoose.model('User');
            const Role = mongoose.model('Role');

            const roles = await Promise.all( // TODO: Rewrite to single query
                obj.rolesId.map(x => Role.findById(x))
            );
            const users = await Promise.all( // TODO: Rewrite to single query
                obj.usersId.map(x => User.findById(x))
            );
            const opinionUsersId = [...new Set([...users, ...roles].filter(x => x && x.manager).map(x => x.manager))];

            obj.opinions = opinionUsersId.map(managerId => ({
                userId: managerId,
                status: 'pending',
            }));
            await obj.save();

            await signals.send('accessRequestCreated', ctx, obj); // TODO: Move to lib/resources.js as generic

            ctx.obj = ctx.body = obj;
        },
    },
    get: {},
    update: {},
    delete: {},
    subs: {
        Opinion: OpinionResource,
    },
});

module.exports = (basePath, options) => createService(basePath, 'AccessRequest', AccessRequestResource, options);
