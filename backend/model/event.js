'use strict';
const mongoose = require('mongoose');
const {getStatusType} = require('../lib/model/types');
const {commonSchema} = require('../lib/model/common');

const eventType = ['accepted', 'created', 'rejected', 'queued', 'done', 'error'];

const schema = Object.assign({
    status: getStatusType(eventType),
    result: {},
    finishedAt: {
        type: Date,
        required: false,
    },
}, commonSchema);

const eventSchema = new mongoose.Schema(schema);

module.exports = eventSchema;
