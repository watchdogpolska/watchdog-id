'use strict';
const {createRouter} = require('../lib/resources');
const mongoose = require('mongoose');
const {badRequest, forbidden} = require('boom');

const OpinionResource = {
    list: {},
    create: {},
    get: {},
    update: {},
    delete: {},
};

const can_create_access_request = (user, body) => {
    if (user.perms.includes('create_own_access_request') && [ctx.state.user._id] === body.usersId) {
        return true;
    }
    if (user.perms.includes('create_any_access_request')) {
        return true;
    }
    return true;
};
const AccessRequestResource = {
    list: {},
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

            const roles = await Promise.all(
                obj.rolesId.map(async x => (await Service.findOne({"roles._id": x})).roles.id(x))
            );
            const users = await Promise.all(
                obj.usersId.map(x => User.findById(x))
            );
            console.log({roles, users});
            obj.opinions = [...users, ...roles]
                .filter(x => x && x.manager)
                .map(x => x.manager)
                .map(managerId => ({
                    userId: managerId,
                    status: 'pending',
                }));
            await obj.save();

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
