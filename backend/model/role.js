'use strict';
const {getStatusType} = require('../lib/model/types');

const mongoose = require('mongoose');

const {roleStatus} = require('../lib/model/status');
const {commonSchema} = require('../lib/model/common');

const schema = Object.assign({
    serviceId: {
        type: mongoose.Schema.ObjectId,
        ref: 'Role',
        required: true,
    },
    title: String,
    description: String,
    manager: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
        required: true,
    },
    status: getStatusType(roleStatus, 'active'),
}, commonSchema);

const roleSchema = new mongoose.Schema(schema);

module.exports = roleSchema;
