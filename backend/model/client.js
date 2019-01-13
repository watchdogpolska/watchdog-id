'use strict';
const mongoose = require('mongoose');
const {commonSchema} = require('../lib/model/common');
const crypto = require('crypto');

const schema = new mongoose.Schema(Object.assign({
    name: String,
    redirect_uri: [
        {
            type: String,
        },
    ],
    secret: {
        type: String,
        unique: true,
        default: () => crypto.randomBytes(16).toString('hex'),
        select: false,
    },
    // confidental: {
    //     type: boolean,
    //     default: true
    // }
}, commonSchema));

schema.virtual('client_secret').get(async function () {
    return this.secret;
});

module.exports = schema;