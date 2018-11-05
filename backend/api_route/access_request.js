'use strict';
const {createRouter} = require('../lib/resources');
const mongoose = require('mongoose');
const {badRequest, forbidden} = require('boom');
const signals = require('../lib/signals');

const OpinionResource = {
    list: {},
    create: {},
    get: {},
    update: {},
    delete: {},
};

const can_create_access_request = (user, body) => {
    if (user.perms.includes('create_own_access_request') && [user._id] === body.usersId) {
        return true;
    }
    if (user.perms.includes('create_any_access_request')) {
        return true;
    }
    return true;
};

const AccessRequestResource = {
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
                query = Object.assign({}, query, {'opinions.userId': {$in: ctx.query.opinionUserId}});
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
            });
            const User = mongoose.model('User');
            const Service = mongoose.model('Service');

            const roles = await Promise.all( // TODO: Rewrite to single query
                obj.rolesId.map(async x => (await Service.findOne({'roles._id': x})).roles.id(x))
            );
            const users = await Promise.all( // TODO: Rewrite to single query
                obj.usersId.map(x => User.findById(x))
            );
            const opinionUsers = [...new Set([...users, ...roles].filter(x => x && x.manager))];

            obj.opinions = opinionUsers.map(managerId => ({
                userId: managerId,
                status: 'pending',
            }));
            await obj.save();

            await signals.send('accessRequestCreated', ctx, obj);
            ctx.body = obj.toJSON();
        },
    },
    get: {},
    update: {},
    delete: {},
    subs: {
        Opinion: OpinionResource,
    },
};

module.exports = () => createRouter('AccessRequest', AccessRequestResource);
