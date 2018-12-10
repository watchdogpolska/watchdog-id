'use strict';
const Router = require('koa-router');
const mongoose = require('mongoose');
const {badRequest, unauthorized, notFound} = require('boom');
const settings = require('../settings');
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const verify = promisify(jwt.verify);

const authenticateClient = Client => async (ctx, next) => {
    const client = await Client.findOne({
        _id: ctx.request.body.client_id,
        secret: ctx.request.body.client_secret
    });

    if (!client) {
        throw badRequest("Invalid 'client_secret' or 'client_id'.")
    }

    ctx.state.client = client;
    return next();
};

const validGrantType = async (ctx, next) => {
    if (!['code', 'refresh_token', 'authorization_code'].includes(ctx.request.body.grant_type)) {
        throw badRequest("Invalid 'grant_type'.")
    }
    return next();
};

const validAuthorizationCode = Authorization => async (ctx, next) => {
    let claim = null;

    if (['code', 'authorization_code'].includes(ctx.request.body.grant_type)) {
        claim = await verify(ctx.request.body.code, settings.JWT_SECRET, {
            audience: 'authorization_code'
        });
    }

    if (ctx.request.body.grant_type === 'refresh_token') {
        claim = await verify(ctx.request.body.refresh_token, settings.JWT_SECRET, {
            audience: 'refresh_token'
        });
    }

    ctx.state.authorization = await Authorization
        .findOne({_id: claim.sub, client: ctx.state.client._id})
        .populate('user');
    if (!ctx.state.authorization) {
        throw unauthorized("Client no longer authorized.");
    }
    return next();
};


const response_types_values = {
    id_token: async authorization => ({
        id_token: await authorization.id_token,
    }),
    code: async authorization => ({
        code: (await authorization.grant).code
    }),
    token: async authorization => {
        const access_token = await authorization.access_token;
        return {
            access_token: access_token.code,
            token_type: "Bearer",
            expires_in: access_token.expiresAt
        }
    },
    none: () => {
    },
};

module.exports = () => {
    const router = new Router();
    const Authorization = mongoose.model('Authorization');
    const Client = mongoose.model('Client');

    router.use(async (ctx, next) => {
        ctx.response.headers['Cache-Control'] = 'no-store';
        ctx.response.headers['Pragma'] = 'no-cache';
        return next();
    });


    router.post('/authorize', async (ctx) => {
        // authorization endpoint
        if (!ctx.request.body.response_type) {
            throw badRequest("Missing 'response_type'")
        }
        console.log("Reach authorization endpoint");

        const req_types = ctx.request.body.response_type.split(' ');
        for (const response_type of req_types) {
            if (!response_types_values[response_type]) {
                throw badRequest("Unsupported 'response_type'.")
            }
        }

        const client = await Client.findById(ctx.request.body.client_id);
        if (!client) {
            throw badRequest("Invalid 'client_id'.")
        }
        if (!client.redirect_uri.includes(ctx.request.body.redirect_uri)) {
            throw badRequest("Invalid 'redirect_uri'.")
        }
        ctx.state.redirect_uri = ctx.request.body.redirect_uri;
        const authorization = Authorization({
            client: client._id,
            scope: ctx.request.body.scope.split(' '),
            user: ctx.state.user,
            redirect_uri: ctx.state.redirect_uri
        });
        await authorization.save();

        const query = Object.assign({}, ...(await Promise.all(
            req_types.map(type => response_types_values[type](authorization))
        )));
        query.state = ctx.request.body.state;
        const url = new URL(client.redirect_uri);

        if (req_types.includes('id_token') || req_types.includes('token')) {
            url.hash = new URLSearchParams(query).toString();
        } else {
            url.search = new URLSearchParams(query);
        }

        const callback_url = url.toString();
        ctx.redirect(callback_url);

    });


    router.post('/token',
        // token endpoint
        validGrantType,
        authenticateClient(Client),
        validAuthorizationCode(Authorization),
        async (ctx, next) => {
            const resp = {
                authorization: ctx.state.authorization,
                access_token: await ctx.state.authorization.access_token,
                refresh_token: await ctx.state.authorization.refresh_token,
                token_type: "Bearer",
                client: ctx.state.client,
            };
            if (ctx.state.authorization.scope.includes('openid')) {
                resp.id_token = await ctx.state.authorization.id_token
            }
            ctx.body = resp;
        });

    router.get('/userinfo', async (ctx, next) => {
        ctx.body = {
            "sub": ctx.state.user._id,
            "email": ctx.state.user.email,
        }
    });
    router.get('/authorization', (ctx, next) => {
        ctx.body = Authorization.find({user: ctx.params.user._id})
    });

    router.post('/authorization', async (ctx, next) => {
        // Basic Auth
        // insert new authorization
        const authorization = Authorization({
            scope: ctx.request.body.scope,
            user: ctx.state.user
        });
        await authorization.save();

        ctx.body = {
            authorization: authorization,
            access_token: await authorization.access_token,
            refresh_token: await authorization.refresh_token,
            token_type: "Bearer",
            user: authorization.user,
        };
    });

    router.get('/authorization/:authorization_id/', async (ctx, next) => {
        ctx.body = await Authorization.findOne({
            user: ctx.state.user._id,
            _id: ctx.params.authorization_id
        })
    });

    router.delete('/authorization/:authorization_id', async (ctx, next) => {
        const authorization = await Authorization.findOne({
            user: ctx.state.user._id,
            _id: ctx.params.authorization_id
        });
        if (!authorization) {
            return notFound("")
        }
        await authorization.remove();
        ctx.body = authorization;
    });

    return router;
};


