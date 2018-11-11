'use strict';
const mongoose = require('mongoose');
const {getStatusType} = require('./lib/types');
const {commonSchema} = require('./lib/common');

const eventType = ['accepted', 'created', 'rejected', 'queued', 'done', 'error'];

const schema = Object.assign({
    status: getStatusType(eventType),
    result: {},
    finishedAt: {
        type: Date,
        required: false
    }
}, commonSchema);
const eventSchema = new mongoose.Schema(schema);


module.exports = eventSchema;
