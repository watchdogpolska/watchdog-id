'use strict';
const send = require('koa-send');
const fs = require('fs');
const util = require('util');
const readFile = util.promisify(fs.readFile);
const path = require('path');

const swaggerUiAssetPath = require('swagger-ui-dist').getAbsoluteFSPath();

const {authMiddleware} = require('../../lib/auth');
// const {requestSchemaMiddleware, responseSchemaMiddleware} = require('./../schema.js');

const toArray = value => Array.isArray(value) ? value : [value];

function wrapHandler(action) {

    return [
        // TODO: Validate requests
        // requestSchemaMiddleware(action.requestBody),
        // responseSchemaMiddleware(action.responses),
        authMiddleware(action.security),
        ...toArray(action.handler),
    ];
}

const getUiHtml = (file, apiDocsPath, schema) => readFile(path.join(__dirname, file), 'utf-8')
    .then(tmpl => tmpl
        .replace('${UI_TITLE}', schema.info.title)
        .replace('${UI_DOCS_PATH}', apiDocsPath)
    );

const serverHtml = ctx => html => {
    ctx.type = 'text/html; charset=utf-8';
    ctx.body = html;
    ctx.status = 200;
};
module.exports = (options = {}) => {
    const apiDocsPath = options.apiDocs || '/apiDocs';
    const swaggerUiPath = options.swaggerUiPath;
    const redocUiPath = options.redocUiPath;

    const router = options.router;
    const paths = {};
    const schemas = {};
    const info = options.info || {};

    const securitySchemes = options.securitySchemes || {
        basicAuth: {
            type: 'http',
            scheme: 'basic',
        },
        bearerAuth: {
            type: 'http',
            scheme: 'bearer',
        },
        apiKeyAuth: {
            type: 'apiKey',
            in: 'header',
            name: 'x-auth-token',
        },
        cookieAuth: {
            type: 'apiKey',
            in: 'cookie',
            name: 'token',
        },
    };

    const security = options.security || Object
        .keys(securitySchemes)
        .map(security => ({[security]: []}));

    const getSchema = () => ({
        openapi: '3.0.0',
        info: {
            title: info.title || info.name,
            description: info.description,
            version: info.version,
        },
        paths: paths,
        components: {
            securitySchemes: securitySchemes,
            schemas: schemas,
        },
        security: security,
    });

    if (redocUiPath) {
        router.get(redocUiPath, ctx => getUiHtml('ui-redoc.html', apiDocsPath, getSchema()).then(serverHtml(ctx)));
    }
    if (swaggerUiPath) {
        router.get(swaggerUiPath, ctx => getUiHtml('ui-swagger.html', apiDocsPath, getSchema()).then(serverHtml(ctx)));
        router.get(`${swaggerUiPath}/:path`, ctx => send(ctx, ctx.params.path, {
            root: swaggerUiAssetPath,
        }));
    }

    router.get('/apiDocs', ctx => {
        ctx.type = 'application/json; charset=utf-8';
        ctx.body = getSchema();
    });

    return {
        getSchema,
        addSchema: (name, new_schema) => {
            schemas[name] = new_schema;
        },
        addEndpoint: (action) => {
            if (!action.url) {
                console.debug('Unknown URL for action.', action);
                return;
            }
            if (!action.method) {
                console.debug(`Unknown action method '${action.method}' for URL '${action.url}'.`, action);
                return;
            }
            if (!paths[action.url]) paths[action.url] = {};
            action.responseType = action.responseType || ['application/json'];
            action.requestType = action.requestType || ['application/json'];

            if (!action.requestBody && action.requestSchema) {
                action.requestBody = action.requestBody || {
                    required: true,
                    content: Object.assign(...action.requestType.map(type => ({[type]: {schema: action.requestSchema}}))),
                };
            }

            paths[action.url][action.method] = {
                responses: action.responses,
                description: action.description,
                requestBody: action.requestBody,
                security: action.security,
                tags: action.tags,
                parameters: action.parameters,
            };
            router[action.method](
                action.url,
                ...wrapHandler({
                    handler: action.handler,
                    responses: action.responses,
                    requestBody: action.requestBody,
                    parameters: action.parameters,
                    security: action.security || options.security,
                })
            );
        },
    };
};
