'use strict';
const mongoose = require('mongoose');
const {serviceStatus} = require("./lib/status");
const {getStatusType} = require("./lib/types");
const {commonSchema} = require("./lib/common");
const JSONWebKey = require( 'json-web-key' );

const serviceSchema = new mongoose.Schema(Object.assign({
    title: String,
    description: String,
    endpointUrl: String,
    status: getStatusType(serviceStatus),
    features: {
        passwordReset: Boolean,
        userProvidedUsername: Boolean
    },
    key: {
        type: String,
        get: (data) => {
            try {
                return JSONWebKey.fromJSON(JSON.parse(data));
            } catch {
                return data;
            }
        },
        set: (data) => JSON.stringify(data),
        validator: (v) => {
            try {
                JSONWebKey.fromJSON(v);
                return true;
            }catch {
                return false;
            }
        },
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
