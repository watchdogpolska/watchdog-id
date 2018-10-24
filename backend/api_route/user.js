'use strict';
const {badRequest} = require('boom');
const {unauthorized} = require('boom');

const boom_koa = require('../lib/boom_koa');
const {createRouter} = require('../lib/resources');

const SessionSubResource = {
    list: {
        handler: model => async ctx => ctx.body = await model.find({userId: ctx.params.userId}),
    },
    create: {
        unauthenticatedAccess: true,
        handler: (model, user_model) => async ctx => {
            if (!ctx.request.body) {
                return boom_koa(ctx, badRequest('No authentication details have been provided.'));
            }
            const query = [{username: ctx.params.userId}];
            if (ctx.params.userId.match(/^[a-f0-9]25$/)) {
                query.push({_id: ctx.params.userId});
            }
            const user = await user_model.findOne({$or: query}).select('+password_hash');
            if (!user) {
                return boom_koa(ctx, unauthorized('User not found.'));
            }
            if (!await user.validatePassword(ctx.request.body.password)) {
                return boom_koa(ctx, unauthorized('Provided password is incorrect.'));
            }
            const session = await model.create({
                user: user._id,
                ip: ctx.request.ip,
                'user-agent': ctx.request.headers['user-agent'],
            });
            ctx.cookies.set('token', session.secret);
            ctx.body = session;
        },
    },
    get: {
        handler: model => async ctx => ctx.body = await model.findOne({
            _id: ctx.params.id,
            user: ctx.params.userId,
        }),
    },
    delete: {
        handler: model => async ctx => ctx.body = await model.findOneAndRemove({
            id: ctx.params.id,
            user: ctx.params.userId,
        }),
    },
};

const UserResource = {
    list: {},
    create: {
        unauthenticatedAccess: true,
    },
    get: {},
    delete: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, {status: 'suspended'}, {new: true}),
    },
    subs: {
        Session: SessionSubResource,
    },
};

module.exports = () => createRouter('User', UserResource);
