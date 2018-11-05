'use strict';
const {badRequest} = require('boom');
const {unauthorized} = require('boom');
const {createRouter} = require('../lib/resources');

const SessionSubResource = {
    list: {
        handler: model => async ctx => ctx.body = await model.find({userId: ctx.params.userId}),
    },
    create: {
        unauthenticatedAccess: true,
        handler: (model, user_model) => async ctx => {
            if (!ctx.request.body) {
                throw badRequest('No authentication details have been provided.');
            }
            const query = [{username: ctx.params.userId}];
            if (ctx.params.userId.match(/^[a-f0-9]25$/)) {
                query.push({_id: ctx.params.userId});
            }
            const user = await user_model.findOne({$or: query}).select('+password_hash');

            if (!user) {
                throw unauthorized('User not found.');
            }

            if (!user.active) {
                throw unauthorized('User account is not active.');
            }
            if (!await user.validatePassword(ctx.request.body.password)) {
                throw unauthorized('Provided password is incorrect.');
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
        req_schema: () => ({
            $async: true,
            type: 'object',
            properties: {
                first_name: {type: 'string'},
                second_name: {type: 'string'},
                username: {type: 'string'},
                password: {type: 'string'},
                email: {type: 'string'},
            },
            required: ['first_name', 'second_name', 'username', 'password', 'email'],
        }),
        res_schema: () => ({
            $async: true,
            type: 'object',
            properties: {
                _id: {type: 'string'},
                first_name: {type: 'string'},
                second_name: {type: 'string'},
                username: {type: 'string'},
                email: {type: 'string'},
                status: {type: 'string'},
            },
            required: ['_id', 'first_name', 'second_name', 'username', 'email', 'status'],
        }),
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
