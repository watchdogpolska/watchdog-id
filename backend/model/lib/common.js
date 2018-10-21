'use strict';
const mongoose = require('mongoose');

const commonSchema = {
    createdAt: Date,
    createdBy: mongoose.Schema.ObjectId,
    modifiedAt: Date,
    modifiedBy: mongoose.Schema.ObjectId
};

module.exports = {
    commonSchema
};
