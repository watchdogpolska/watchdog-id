'use strict';
const mongoose = require('mongoose');
const {badRequest, unauthorized} = require('boom');
const settings = require('../settings');
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const verify = promisify(jwt.verify);

const authenticateClient = Client => async (ctx, next) => {
    const client = await Client.findOne({
        _id: ctx.request.body.client_id,
        secret: ctx.request.body.client_secret,
    });

    if (!client) {
        throw badRequest("Invalid 'client_secret' or 'client_id'.");
    }

    ctx.state.client = client;
    return next();
};

const validGrantType = async (ctx, next) => {
    if (!['code', 'refresh_token', 'authorization_code'].includes(ctx.request.body.grant_type)) {
        throw badRequest("Invalid 'grant_type'.");
    }
    return next();
};

const validAuthorizationCode = Authorization => async (ctx, next) => {
    let claim = null;

    if (['code', 'authorization_code'].includes(ctx.request.body.grant_type)) {
        claim = await verify(ctx.request.body.code, settings.JWT_SECRET, {
            audience: 'authorization_code',
        });
    }

    if (ctx.request.body.grant_type === 'refresh_token') {
        claim = await verify(ctx.request.body.refresh_token, settings.JWT_SECRET, {
            audience: 'refresh_token',
        });
    }

    ctx.state.authorization = await Authorization
        .findOne({_id: claim.sub, client: ctx.state.client._id})
        .populate('user');
    if (!ctx.state.authorization) {
        throw unauthorized('Client no longer authorized.');
    }
    return next();
};


const response_types_values = {
    id_token: async authorization => ({
        id_token: await authorization.id_token,
    }),
    code: async authorization => ({
        code: (await authorization.grant).code,
    }),
    token: async authorization => {
        const access_token = await authorization.access_token;
        return {
            access_token: access_token.code,
            token_type: 'Bearer',
            expires_in: access_token.expiresAt,
        };
    },
    none: () => {
    },
};

const authorizeEndpoint = (Client, Authorization) => async (ctx) => {
    // authorization endpoint
    if (!ctx.request.body.response_type) {
        throw badRequest("Missing 'response_type'");
    }

    const req_types = ctx.request.body.response_type.split(' ');
    for (const response_type of req_types) {
        if (!response_types_values[response_type]) {
            throw badRequest("Unsupported 'response_type'.");
        }
    }

    const client = await Client.findById(ctx.request.body.client_id);
    if (!client) {
        throw badRequest("Invalid 'client_id'.");
    }
    if (!client.redirect_uri.includes(ctx.request.body.redirect_uri)) {
        throw badRequest("Invalid 'redirect_uri'.");
    }
    ctx.state.redirect_uri = ctx.request.body.redirect_uri;

    const authorization = Authorization({
        client: client._id,
        scope: ctx.request.body.scope.split(' '),
        user: ctx.state.user._id,
        redirect_uri: ctx.state.redirect_uri,
    });
    await authorization.save();

    const query = Object.assign({}, ...await Promise.all(
        req_types.map(type => response_types_values[type](authorization))
    ));
    query.state = ctx.request.body.state;
    const url = new URL(client.redirect_uri);

    if (req_types.includes('id_token') || req_types.includes('token')) {
        url.hash = new URLSearchParams(query).toString();
    } else {
        url.search = new URLSearchParams(query);
    }

    const callback_url = url.toString();
    ctx.redirect(callback_url);
};

const tokenEndpoint = async ctx => {
    const resp = {
        authorization: ctx.state.authorization,
        access_token: await ctx.state.authorization.access_token,
        refresh_token: await ctx.state.authorization.refresh_token,
        token_type: 'Bearer',
        client: ctx.state.client,
    };
    if (ctx.state.authorization.scope.includes('openid')) {
        resp.id_token = await ctx.state.authorization.id_token;
    }
    ctx.body = resp;
};

const userInfoEndpoint = async ctx => {
    ctx.body = {
        sub: ctx.state.user._id,
        email: ctx.state.user.email,
    };
};

const cacheMiddleware = async (ctx, next) => {
    ctx.response.headers['Cache-Control'] = 'no-store';
    ctx.response.headers.Pragma = 'no-cache';
    return next();
};

module.exports = (basePath, schema) => {
    const Authorization = mongoose.model('Authorization');
    const Client = mongoose.model('Client');

    schema.addEndpoint({
        url: `${basePath}/authorize`,
        description: 'Authorize application',
        operationId: 'oauth2_authorize',
        tags: ['OAuth 2'],
        method: 'post',
        handler: [
            cacheMiddleware,
            authorizeEndpoint(Client, Authorization),
        ],
        responses: {
            200: {
                description: 'authorization success response',
                content: {
                    'application/json': {
                        schema: {
                            type: 'object',
                            properties: {
                                authorization: {type: 'string'},
                                access_token: {type: 'string'},
                                refresh_token: {type: 'string'},
                                token_type: {type: 'string'},
                            },
                        },
                    },
                },
            },
        },
        requestSchema: {
            type: 'object',
            properties: {
                response_type: {type: 'string'},
                scope: {type: 'string'},
                redirect_uri: {type: 'string'},
                client_id: {type: 'string'},
            },
        },
    });

    schema.addEndpoint({
        method: 'post',
        url: `${basePath}/token`,
        description: 'Achieve access token',
        operationId: 'oauth2_token',
        tags: ['OAuth 2'],
        requestSchema: {
            $ref: '#/components/schemas/Authorization',
        },
        responses: {
            200: {
                description: 'an authorization object',
                content: {
                    'application/json': {
                        schema: {
                            $ref: '#/components/schemas/Authorization',
                        },
                    },
                },
            },
        },
        handler: [
            validGrantType,
            authenticateClient(Client),
            validAuthorizationCode(Authorization),
            tokenEndpoint,
        ],
    });

    schema.addEndpoint({
        method: 'get',
        url: `${basePath}/userinfo`,
        description: 'Receive user info',
        operationId: 'userinfo',
        tags: ['OAuth 2'],
        responses: {
            200: {
                description: 'a userinfo',
                content: {
                    'application/json': {
                        schema: {
                            type: 'string',
                            properties: {
                                sub: {type: 'string'},
                                email: {type: 'string'},
                            },
                        },
                    },
                },
            },
        },
        handler: userInfoEndpoint,
    });
};


