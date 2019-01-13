'use strict';
const mongoose = require('mongoose');
const settings = require('../settings');
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const sign = promisify(jwt.sign);

const schema = new mongoose.Schema({
    client: {
        type: mongoose.Schema.ObjectId,
        ref: 'Client',
        required: false,
    },
    scope: [
        {
            type: String,
            enum: Object.keys(require('./scopes.js')),
        },
    ],
    redirect_uri: {
        type: String,
    },
    user: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
        required: true,
    },
    description: {
        type: String,
    },
});

schema.virtual('grant').get(async function () {
    const exp = Math.floor(Date.now() / 1000) + 5 * 60;
    const code = await sign({
        sub: this._id,
        aud: 'authorization_code',
        iss: settings.JWT_ISSUER,
    }, settings.JWT_SECRET);

    return {
        code: code,
        expiresAt: exp,
    };
});

schema.virtual('access_token').get(async function () {
    const exp = Math.floor(Date.now() / 1000) + 60 * 60;
    const code = await jwt.sign({
        sub: this._id,
        aud: 'access_token',
        iss: settings.JWT_ISSUER,
    }, settings.JWT_SECRET);

    return {
        token: code,
        expiresAt: exp,
    };
});

schema.virtual('id_token').get(async function () {
    return await jwt.sign({
        sub: this.user._id,
        aud: this.client._id,
        iss: settings.JWT_ISSUER,
    }, settings.JWT_SECRET);
});
schema.virtual('refresh_token').get(async function () {
    const exp = Math.floor(Date.now() / 1000) + 24 * 60;
    const code = await jwt.sign({
        sub: this._id,
        aud: 'refresh_token',
    }, settings.JWT_SECRET);

    return {
        token: code,
        expiresAt: exp,
    };
});

module.exports = schema;
