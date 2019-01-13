'use strict';
const {isBoom} = require('boom');

module.exports = () => async (ctx, next) => {
    try {
        return await next();
    } catch (err) {
        if (!isBoom(err)) throw err;
        console.error('Boom error', err.message);
        ctx.response.status = err.output.statusCode;
        ctx.response.set(err.output.headers);
        ctx.response.body = err.output.payload;
    }
};
