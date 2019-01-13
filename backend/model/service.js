'use strict';
const mongoose = require('mongoose');
const {serviceStatus} = require('../lib/model/status');
const {getStatusType} = require('../lib/model/types');
const {commonSchema} = require('../lib/model/common');
const JSONWebKey = require('json-web-key');

const serviceSchema = new mongoose.Schema(Object.assign({
    title: String,
    description: String,
    endpointUrl: String,
    status: getStatusType(serviceStatus),
    features: {
        passwordReset: Boolean,
        userProvidedUsername: Boolean,
    },
    key: {
        type: String,
        get: function (data) {
            try {
                return JSONWebKey.fromJSON(JSON.parse(data));
            } catch (err) {
                return data;
            }
        },
        set: (data) => JSON.stringify(data),
        validator: (v) => {
            try {
                JSONWebKey.fromJSON(v);
                return true;
            } catch (err) {
                return false;
            }
        },
    },
}, commonSchema));

serviceSchema.virtual('active').get(function () {
    return this.status === 'active';
});

module.exports = serviceSchema;
