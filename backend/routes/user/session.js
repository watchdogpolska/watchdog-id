'use strict';
const factory = require('./../../factory');
const {badRequest} = require('boom');
const {unauthorized} = require('boom');

module.exports = () => ({
    schemas: {
        Session: {
            type: 'object',
            properties: {
                id: {
                    type: 'integer',
                    readOnly: true,
                },
                user: {
                    type: 'string',
                },
                secret: {
                    type: 'string',
                },
                userAgent: {
                    type: 'string',
                },
                ip: {
                    type: 'string',
                },
                createdAt: {
                    type: 'string',
                },
                expiresAt: {
                    type: 'string',
                },
            },
        },
    },
    list: {
        handler: model => async ctx => ctx.body = await model.find({userId: ctx.params.userId}),
    },
    create: {
        security: [],
        requestBody: {
            required: true,
            content: {
                'application/json': {
                    schema: {
                        type: 'object',
                        properties: {
                            password: {
                                type: 'string',
                            },
                        },
                    },
                },
            },
        },
        handler: (model, user_model) => async ctx => {
            if (!ctx.request.body) {
                throw badRequest('No authentication details have been provided.');
            }
            const query = [{username: ctx.params.userId}];

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
            await factory.enforceFactorRequest(ctx);

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
});

