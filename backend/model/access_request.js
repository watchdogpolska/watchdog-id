'use strict';
const {commonSchema }= require('../lib/model/common');
const eventSchema = require('./event');
const opinionSchema = require('./opinion');
const mongoose = require('mongoose');


const schema = Object.assign({
    name: String,
    opinions: [opinionSchema],
    events: [eventSchema],
    usersId: [{
        type: mongoose.Schema.ObjectId,
        ref: 'User',
    }],
    rolesId: [{
        type: mongoose.Schema.ObjectId,
        ref: 'Role',
    }],
}, commonSchema);

const accessRequestSchema = new mongoose.Schema(schema);

accessRequestSchema.virtual('status').get(function () {
    for (const status of eventSchema.obj.status.enum) {
        if (this.opinions.some(opinion => opinion.status === status)) {
            return status;
        }
    }
    return 'unknown';
});

module.exports = accessRequestSchema;
