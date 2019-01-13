'use strict';
const Ajv = require('ajv');
const {badRequest} = require('boom');
const {badImplementation, unsupportedMediaType} = require('boom');

const ajv = new Ajv({
    removeAdditional: 'all',
    useDefaults: true,
    allErrors: true,
});

const requestSchemaMiddleware = requestBody => async (ctx, next) => {
    if (!requestBody) return await next();
    // console.log({content:requestBody.content});
    // const requestType = Object.keys(requestBody.content || {}).find(ctx.request.is);
    // console.log({requestType});
    const requestType = 'application/json';
    if (!requestType) {
        throw unsupportedMediaType('That request media is not supported.');
    }
    try {
        const requestSchema = requestBody.content[requestType].schema;
        ctx.request.body = await ajv.validate(requestSchema, ctx.request.body);
    } catch (err) {
        if (!(err instanceof Ajv.ValidationError)) throw err;
        if (requestBody.content[requestType].required) {
            throw badRequest(ajv.errorsText(err.errors));
        }
        ctx.request.body = {};
    }
    return await next();
};

const responseSchemaMiddleware = responses => async (ctx, next) => next().then(async () => {
    if (!responses) return await next();

    const statusCode = ctx.status;
    const responseType = Object
        .keys(responses[statusCode].content)
        .find(ctx.request.accepts);

    if (!responseType) {
        throw unsupportedMediaType('No available response media is not supported');
    }

    const responseSchema = responseType.schema;

    if (ctx.body.toJSON) {
        // TODO: How to remove that hack?
        ctx.body = JSON.parse(JSON.stringify(ctx.body.toJSON()));
    }

    try {
        ctx.body = await ajv.validate(responseSchema, ctx.body);
    } catch (err) {
        if (!(err instanceof Ajv.ValidationError)) throw err;
        throw badImplementation(ajv.errorsText(err.errors));
    }
});

module.exports = {
    requestSchemaMiddleware,
    responseSchemaMiddleware,
    ajv,
};
