'use strict';
const camelCase = require('camelcase');
const mongoose = require('mongoose');
const {notFound} = require('boom');
const humanizeString = require('humanize-string');

const standardParam = name => ({
    in: 'path',
    name: 'id',
    schema: {
        type: 'string',
    },
    required: true,
    description: `The ${name} ID`,
});

const getDefaultResource = name => ({
    list: {
        handler: model => async ctx => ctx.body = await model.find(),
        path: '',
        method: 'get',
        responses: {
            200: {
                description: `a ${name} object`,
                content: {
                    'application/json': {
                        schema: {
                            type: 'array',
                            items: {
                                $ref: `#/components/schemas/${name}`,
                            },
                        },
                    },
                },
            },
        },
    },
    create: {
        handler: model => async ctx => ctx.body = await model.create(ctx.request.body),
        // req_schema: (ctx) => { ... },
        path: '',
        method: 'post',
        requestSchema: {
            $ref: `#/components/schemas/${name}`,
        },
        responses: {
            200: {
                description: `a ${name} object`,
                content: {
                    'application/json': {
                        schema: {
                            $ref: `#/components/schemas/${name}`,
                        },
                    },
                },
            },
        },
    },
    get: {
        handler: model => async ctx => {
            ctx.entry = await model.findOne({_id: ctx.params.id});
            if (!ctx.entry) {
                throw notFound('Unable to found entry');
            }
            ctx.body = ctx.entry.toJSON({virtuals: true});
        },
        path: ':id',
        method: 'get',
        parameters: [
            standardParam(name),
        ],
        responses: {
            200: {
                description: `a ${name} object`,
                content: {
                    'application/json': {
                        schema: {
                            $ref: `#/components/schemas/${name}`,
                        },
                    },
                },
            },
        },
    },
    update: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, ctx.request.body, {new: true}),
        path: ':id',
        method: 'post',
        parameters: [standardParam(name)],
        requestSchema: {
            $ref: `#/components/schemas/${name}`,
        },
        responses: {
            200: {
                description: `a ${name} object`,
                content: {
                    'application/json': {
                        schema: {
                            $ref: `#/components/schemas/${name}`,
                        },
                    },
                },
            },
        },
    },
    delete: {
        handler: model => async ctx => ctx.body = await model.findOneAndUpdate({_id: ctx.params.id}, {status: 'suspended'}, {new: true}),
        path: ':id',
        method: 'delete',
        parameters: [
            standardParam(name),
        ],
        responses: {
            200: {
                description: `a ${name} object`,
                content: {
                    'application/json': {
                        schema: {
                            $ref: `#/components/schemas/${name}`,
                        },
                    },
                },
            },
        },
    },
});

const toTitle = text => text.substring(0, 1).toUpperCase() + text.substring(1);

const createService = (basePath, name, getCustomResource, schema, options = {}) => {
    const defaultResource = getDefaultResource(name);
    const customResource = getCustomResource(name);
    const model = mongoose.model(name);
    const defaultParameters = options.parameters || [];
    const parents = options.parents || [];
    const tags = options.tags || [humanizeString(name)];
    Object
        .keys(defaultResource)
        .filter(action_name => Object.keys(customResource).includes(action_name))
        .map(action_name => Object.assign(
            {
                description: `${toTitle(action_name)} ${humanizeString(name)}`,
                tags: options.tags || [humanizeString(name)],
            },
            defaultResource[action_name],
            customResource[action_name],
        ))
        .forEach(action => schema.addEndpoint({
            url: `${basePath}/${action.path}`,
            method: action.method,
            description: action.description,
            tags: options.tags || tags,
            operationId: action.operationId || camelCase(action.description),
            responses: action.responses,
            requestSchema: action.requestSchema,
            requestBody: action.requestBody,
            security: action.security,
            parameters: [...defaultParameters, ...action.parameters || []],
            handler: action.handler(model, ...parents),
        }));

    Object
        .entries(customResource.subs || {})
        .forEach(([subName, subResource]) => {
            const sub_parameter = {
                in: 'path',
                name: `${camelCase(name)}Id`,
                schema: {
                    type: 'string',
                },
                required: true,
                description: `The ${name} ID`,
            };
            const subBasePath = `${basePath}/:${sub_parameter.name}/${camelCase(subName)}`;
            const subOptions = Object.assign({}, options, {
                basePath: basePath,
                parents: [model, ...parents],
                parameters: [...defaultParameters, sub_parameter],
            });
            createService(subBasePath, subName, subResource, schema, subOptions);
        });

    Object.entries(customResource.actions || {})
        .forEach(([actionName, action]) => {
            const sub_parameter = {
                in: 'path',
                name: `${camelCase(name)}Id`,
                schema: {
                    type: 'string',
                },
                required: true,
                description: `The ${name} ID`,
            };
            schema.addEndpoint({
                method: 'post',
                url: `${basePath}/:${sub_parameter.name}/actions/${actionName}`,
                handler: action.handler(action.model, ...parents),
                description: action.description,
                tags: options.tags || [humanizeString(name)],
                operationId: options.operationId || `${actionName}_${name}`,
                responses: action.responses,
                requestSchema: action.requestSchema,
                requestBody: action.requestBody,
                security: action.security || options.security,
                parameters: [...defaultParameters, sub_parameter],
            });
        });
    if (customResource.schemas) {
        Object.entries(customResource.schemas).forEach((args) => schema.addSchema(...args));
    }
};


module.exports = {
    createService,
};
