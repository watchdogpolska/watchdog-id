'use strict';
const {unauthorized} = require('boom');
const mongoose = require('mongoose');
const settings = require('../settings');
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const verify = promisify(jwt.verify);
const basic_auth = require('basic-auth');
const factory = require('./../factory');

const TokenAuth = async (ctx, token) => {
    if (!token) return;

    const Session = mongoose.model('Session');

    const session = await Session
        .findOneAndUpdate(
            {secret: token, expiresAt: {$lt: new Date()}},
            {expiresAt: new Date(new Date() - settings.SESSION_LIFETIME * 1000)}
        )
        .populate('user').select('store');

    if (!session) return;

    ctx.state.session = session;
    ctx.state.user = session.user;
};

const BearerAuth = async ctx => {
    const Authorization = mongoose.model('Authorization');
    if (!ctx.req.headers.authorization || !ctx.req.headers.authorization.startsWith('Bearer ')) {
        return;
    }
    const auth_header = ctx.req.headers.authorization;

    const token = auth_header.match('Bearer (.+?)$')[1];
    let claim = null;

    try {
        claim = await verify(token, settings.JWT_SECRET, {
            audience: 'access_token',
        });
    } catch (err) {
        throw unauthorized('Access token is no longer valid, probably expired.');
    }

    const authorization = await Authorization
        .findById(claim.sub)
        .populate('user');

    if (!authorization) {
        throw unauthorized('Access token is invalid due to the withdrawal of the authorization');
    }
    ctx.state.user = authorization.user;
};

const BasicAuth = async ctx => {
    const User = mongoose.model('User');
    if (!ctx.request.headers.authorization || !ctx.request.headers.authorization.startsWith('Basic ')) {
        return;
    }

    const user_header = basic_auth(ctx);
    const user = await User.findOne({username: user_header.name}).select('+password_hash');
    if (!user) {
        throw unauthorized('User not found.', 'Basic');
    }
    if (!user.active) {
        throw unauthorized('User account is not active.', 'Basic');
    }
    if (!await user.validatePassword(user_header.pass)) {
        throw unauthorized('Provided password is incorrect.', 'Basic');
    }
    ctx.state.user = user;
    factory.enforceFactorRequest(ctx);
};

//
module.exports = {
    authMiddleware: security => async (ctx, next) => {
        if (!security) return await next();

        if (security.find(x => Object.keys(x).includes('basicAuth'))) {
            // console.log('Test basicAuth');
            await BasicAuth(ctx);
        }
        // console.log({state: ctx.state});

        if (security.find(x => Object.keys(x).includes('apiKeyAuth'))) {
            // console.log('Test apiKeyAuth');
            await TokenAuth(ctx, ctx.req.headers['x-auth-token']);
        }
        // console.log({state: ctx.state});

        if (security.find(x => Object.keys(x).includes('cookieAuth'))) {
            // console.log('Test cookieAuth');
            await TokenAuth(ctx, ctx.cookies.get('token'));
        }
        // console.log({state: ctx.state});

        if (security.find(x => Object.keys(x).includes('bearerAuth'))) {
            // console.log('Test bearerAuth');
            await BearerAuth(ctx);
        }
        // console.log({state: ctx.state});

        // console.log('Request user', ctx.state.user ? ctx.state.user._id : '(anonymous)');
        ctx.isAuthenticated = () => !!ctx.state.user;
        ctx.isUnauthenticated = () => !ctx.state.user;
        return await next();
    },
};
