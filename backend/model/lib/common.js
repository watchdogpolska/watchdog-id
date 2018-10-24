'use strict';
const mongoose = require('mongoose');

const commonSchema = {
    createdAt: {
        type: Date,
        required: true,
        default: Date.now,
    },
    expiresAt: {
        type: Date,
        required: true,
        default: () => new Date(new Date() - 60 * 60 * 1000),
    },
    createdBy: mongoose.Schema.ObjectId,
    modifiedBy: mongoose.Schema.ObjectId,
};

module.exports = {
    commonSchema,
};
