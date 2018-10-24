'use strict';
const {getStatusType} = require("./lib/types");

const mongoose = require('mongoose');

const {roleStatus} = require("./lib/status");
const {commonSchema} = require("./lib/common");

const schema = Object.assign({
    title: String,
    description: String,
    manager: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
        required: true,
    },
    status: getStatusType(roleStatus)
}, commonSchema);

const roleSchema = new mongoose.Schema(schema);

module.exports = roleSchema;
