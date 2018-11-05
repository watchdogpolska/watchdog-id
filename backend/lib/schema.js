'use strict';
const Ajv = require('ajv');
const {badRequest} = require('boom');
const {badImplementation} = require('boom');

const ajv = new Ajv({
    removeAdditional: 'all',
    useDefaults: true,
});

const req_schema_validator = async (ctx, next) => {
    if (!ctx.req_schema) return next();
    try {
        ctx.request.body = await ajv.validate(ctx.req_schema, ctx.request.body);
    } catch (err) {
        if (!(err instanceof Ajv.ValidationError)) throw err;
        throw badRequest(ajv.errorsText(err.errors));
    }
    return next();
};

const res_schema_validator = async (ctx, next) => {
    await next();
    if (!ctx.res_schema) return;
    if (ctx.body.toJSON) {
        // TODO: How to remove that hack?
        ctx.body = JSON.parse(JSON.stringify(ctx.body.toJSON()));
    }
    try {
        ctx.body = await ajv.validate(ctx.res_schema, ctx.body);
    } catch (err) {
        if (!(err instanceof Ajv.ValidationError)) throw err;
        throw badImplementation(ajv.errorsText(err.errors));
    }
};

module.exports = {
    req_schema_validator,
    res_schema_validator,
};
