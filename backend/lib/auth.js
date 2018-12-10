'use strict';
const {unauthorized} = require('boom');
const mongoose = require('mongoose');
const settings = require('../settings');
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const verify = promisify(jwt.verify);
const basic_auth = require('basic-auth');

const session_user = async (ctx, next) => {
    const Session = mongoose.model('Session');
    const token = ctx.req.headers['x-auth-token'] || ctx.cookies.get('token');
    const session = token ? await Session
        .findOneAndUpdate(
            {secret: token, expiresAt: {$lt: new Date()}},
            {expiresAt: new Date(new Date() - settings.SESSION_LIFETIME * 1000)}
        )
        .populate('user') : null;
    ctx.state.session = session;
    ctx.state.user = session ? session.user : null;
};

const authorization_user = async (ctx, next) => {
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
        console.log(err);
        throw unauthorized('Access token is no longers valid, probably expired.');
    }

    const authorization = await Authorization
        .findById(claim.sub)
        .populate('user');

    if (!authorization) {
        throw unauthorized('Access token is invalid due to the withdrawal of the authorization');
    }
    ctx.state.user = authorization.user;
};

const basic_user = async ctx => {
    const User = mongoose.model('User');

    if (!ctx.req.headers.authorization || !ctx.req.headers.authorization.startsWith('Basic ')) {
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
};
module.exports = {
    setUserMiddleware: () => async (ctx, next) => {
        await session_user(ctx);
        await authorization_user(ctx);
        await basic_user(ctx);
        console.log('Request user', ctx.state.user ? ctx.state.user._id : '(anonymous)');
        ctx.isAuthenticated = () => !!ctx.state.user;
        ctx.isUnauthenticated = () => !ctx.state.user;
        return await next();
    },
    authenticatedOnly: async (ctx, next) => {
        if (ctx.isAuthenticated()) {
            return await next();
        }
        throw unauthorized('No authentication details have been provided or incorrect.');
    },
};
