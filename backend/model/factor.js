'use strict';
const {commonSchema} = require('../lib/model/common');
const mongoose = require('mongoose');
const factory = require('../factory');

const factorSchema = new mongoose.Schema(Object.assign({
    name: {
        type: String,
    },
    type: {
        type: String,
        enum: factory.getNames(),
    },
    config: {
        type: mongoose.Schema.Types.Mixed,
    },
    challenge: {
        type: mongoose.Schema.Types.Mixed,
    },
    enabled: {
        type: Boolean,
        default: true,
    },
    verified: {
        type: Boolean,
        default: false,
    },
}, commonSchema));

module.exports = factorSchema;
