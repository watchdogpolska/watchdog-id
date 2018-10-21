'use strict';
const mongoose = require('mongoose');
const {serviceStatus} = require("./lib/status");
const {getStatusType} = require("./lib/types");
const {commonSchema} = require("./lib/common");

const serviceSchema = new mongoose.Schema(Object.assign({
    title: String,
    description: String,
    endpointUrl: String,
    status: getStatusType(serviceStatus),
    features: {
        passwordReset: Boolean,
        userProvidedUsername: Boolean
    },
    roles: [
        require('./role')
    ],
}, commonSchema));

serviceSchema.virtual('active').get(function () {
    return this.status === 'active'
});


serviceSchema.virtual('active').get(function () {
    return this.status === 'active'
});

module.exports = serviceSchema;
