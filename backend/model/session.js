'use strict';
const mongoose = require('mongoose');
const crypto = require('crypto');
const settings = require('../settings');

const sessionSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
        required: true,
    },
    secret: {
        type: String,
        unique: true,
        default: () => crypto.randomBytes(16).toString('hex'),
        select: false,
    },
    'user-agent': String,
    ip: {
        type: String,
        required: true,
    },
    createdAt: {
        type: Date,
        required: true,
        default: Date.now,
    },
    expiresAt: {
        type: Date,
        required: true,
        default: () => new Date(new Date() - settings.SESSION_LIFETIME * 1000),
    },
});

sessionSchema.virtual('active').get(function () {
    return this.expires <= Date.now();
});

module.exports = sessionSchema;
