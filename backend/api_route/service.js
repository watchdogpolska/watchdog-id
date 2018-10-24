const {createRouter} = require('../lib/resources');
const mongoose = require('mongoose');


const RoleResource = {
    list: {
        handler: (model, service_model) => async ctx => {
            const service = await service_model.findOne({_id: ctx.params.serviceId});
            ctx.body = service.roles
        }
    },
    create: {
        handler: (model, service_model) => async ctx => {
            const service = await await service_model.findOneAndUpdate(
                {_id: ctx.params.serviceId},
                {'$push': {roles: ctx.request.body}},
                {new: true}
            );
            ctx.body = service.roles.pop();
        }
    },
    get: {
        handler: (model, service_model) => async ctx => {
            const service = await service_model.findOne({
                _id: ctx.params.serviceId,
                'roles._id': ctx.params._id
            });
            ctx.body = service.find(x => x._id === ctx.params.id);
        }
    },
    update: {
        handler: (model, service_model) => async ctx => {
            const update = {};
            Object.keys(ctx.request.body).forEach(key => {
                update[`roles.$[role].${key}`] = ctx.request.body[key]
            });

            const service = await service_model.findOneAndUpdate(
                {_id: ctx.params.serviceId, 'roles._id': ctx.params.id},
                {'$set': update},
                {
                    arrayFilters: [
                        {'role._id': mongoose.Types.ObjectId(ctx.params.id)}
                    ],
                    new: true
                }
            );
            ctx.body = service.roles.find(x => x._id.toString() === ctx.params.id);
        }
    },
    delete: {
        handler: (model, service_model) => async ctx => {
            await service_model.findOneAndUpdate(
                {_id: ctx.params.serviceId, 'roles._id': ctx.params.id},
                {'$pull': {roles: {'id': ctx.params.id}}},
            );
            ctx.body = {};
        }
    },
};

const ServiceResource = {
    list: {},
    create: {},
    get: {},
    update: {},
    delete: {},
    subs: {
        Role: RoleResource
    }
}

module.exports = () => createRouter('Service', ServiceResource);
