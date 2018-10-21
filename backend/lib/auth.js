const {unauthorized} = require('boom');
const boom_koa = require('./boom_koa');
const mongoose = require('mongoose');

module.exports = ({
    setUserMiddleware: () => async (ctx, next) => {
        const Session = mongoose.model('Session');
        let token = ctx.req.headers['x-auth-token'] || ctx.cookies.get('token');
        const session = await Session.findOne({'secret': token}).populate('user');
        const user = session.user;
        ctx.state.user = user;
        ctx.state.session = session;
        ctx.isAuthenticated = () => !!ctx.state.user;
        ctx.isUnauthenticated = () => !ctx.state.user;
        await next();
    },
    authenticatedOnly: async (ctx, next) => {
        if(ctx.isAuthenticated()){
            return await next();
        }
        await boom_koa(ctx, unauthorized('No authentication details have been provided or incorrect.'));
    }
});
