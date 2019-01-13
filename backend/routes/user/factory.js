'use strict';
const factory = require('./../../factory');

const handleRegistrationVerification = {
    description: 'Verify factor',
    requestSchema: {
        type: 'object',
        writeOnly: true,
        additionalProperties: {
            type: 'string',
        },
    },
    responses: {
        200: {
            description: 'updated Factor',
            content: {
                'application/json': {
                    schema: {
                        $ref: '#/components/schemas/Factor',
                    },
                },
            },
        },
    },
    handler: (model, user_model) => async ctx => {
        const user = user_model.findOne(ctx.params.userId);
        let factory_instance = user.factors.id(ctx.params.id);
        const factor = factory.getAll()[factory_instance.type];
        await factor.registrationVerificationHandler(ctx.state.user, factory_instance, ctx.request.body);
        await factory_instance;
        await user.save();
    },
};


module.exports = () => ({
    schemas: {
        Factor: {
            type: 'object',
            properties: {
                _id: {
                    type: 'string',
                    readOnly: true,
                },
                name: {
                    type: 'string',
                },
                type: {
                    type: 'string',
                    enum: factory.getNames(),
                },
                config: {
                    type: 'object',
                    writeOnly: true,
                    additionalProperties: {
                        type: 'string',
                    },
                },
                challenge: {
                    type: 'object',
                    writeOnly: true,
                    additionalProperties: {
                        type: 'string',
                    },
                },
            },
        },
    },
    create: {
        description: 'Create a factor',
        requestSchema: {
            $ref: '#/components/schemas/Factor',
        },
        responses: {
            200: {
                description: 'A new factor',
                content: {
                    'application/json': {
                        schema: {
                            $ref: '#/components/schemas/Factor',
                        },
                    },
                },
            },
        },
        handler: (model, user_model) => async ctx => {
            const factor = factory.getAll()[ctx.request.body.type];
            const requestInput = ctx.request.body.data || {};
            let factor_instance = new model({
                name: ctx.request.body.name,
                type: factor.name,
                verified: false,
            });
            factor.registrationChallengeHandler(ctx.state.user, factor_instance, requestInput);
            const user = user_model.findOne(ctx.params.userId);
            user.factors.add(factor_instance);
            await factor_instance.save();
            await user.save();
            ctx.body = factor_instance;
        },
    },
    list: {
        handler: (model, user_model) => async ctx => {
            ctx.body = (await user_model.find({userId: ctx.params.userId})).factor;
        },
    },
    get: {
        handler: (model, user_model) => async ctx => ctx.body = await user_model.findOne({
            _id: ctx.params.userId,
        }).id(ctx.params.id),
    },
    delete: {
        handler: (model, user_model) => async ctx => ctx.body = await user_model.find({
            _id: ctx.params.userId,
        }).id(ctx.params.id).remove(),
    },
    actions: {
        verify: handleRegistrationVerification,
    },
});
