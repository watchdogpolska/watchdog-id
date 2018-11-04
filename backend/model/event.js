'use strict';
const mongoose = require('mongoose');
const {getStatusType} = require('./lib/types');
const {commonSchema} = require('./lib/common');

const eventType = ['created', 'accepted', 'rejected', 'queued', 'done', 'error'];

const schema = Object.assign({
    status: getStatusType(eventType),
    data: {},
}, commonSchema);
const eventSchema = new mongoose.Schema(schema);


module.exports = eventSchema;
