'use strict';
const {unauthorized} = require('boom');
const mongoose = require('mongoose');
const settings = require('../settings');

module.exports = {
    setUserMiddleware: () => async (ctx, next) => {
        const Session = mongoose.model('Session');
        const token = ctx.req.headers['x-auth-token'] || ctx.cookies.get('token');
        const session = token ? await Session
            .findOneAndUpdate(
                {secret: token, expiresAt: {$lt: new Date()}},
                {expiresAt: new Date(new Date() - settings.SESSION_LIFETIME * 1000)}
            )
            .populate('user') : null;
        ctx.state.user = session ? session.user : null;
        ctx.state.session = session;
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
