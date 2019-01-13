'use strict';
const mongoose = require('mongoose');

const commonSchema = {
    createdAt: {
        type: Date,
        required: true,
        default: Date.now,
    },
    modifiedAt: {
        type: Date,
        required: true,
        default: Date.now,
    },
    createdBy: mongoose.Schema.ObjectId,
    modifiedBy: mongoose.Schema.ObjectId,
};

module.exports = {
    commonSchema,
};
