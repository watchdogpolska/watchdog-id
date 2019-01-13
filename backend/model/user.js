'use strict';
const {EmailType} = require('../lib/model/types');

const {commonSchema} = require('../lib/model/common');
const {getStatusType} = require('../lib/model/types');
const mongoose = require('mongoose');
const scrypt = require('scrypt');

const scryptParameters = scrypt.paramsSync(0.1);

const userRoles = {
    pending: {
        active: false,
        perms: [],
    },
    accepted: {
        active: true,
        perms: ['create_own_access_request'],
    },
    admin: {
        active: true,
        perms: [
            'create_any_access_request',
            'change_any_opinion',
        ],
    },
    suspended: {
        active: true,
        perms: [],
    },
};

const userStatus = Object.keys(userRoles);

const schema = Object.assign({
    username: {
        type: String,
        unique: true,
        required: true,
    },
    email: EmailType,
    first_name: {
        type: String,
        required: true,
    },
    second_name: {
        type: String,
        required: true,
    },
    password_hash: {
        type: String,
        required: true,
        select: false,
    },
    manager: {type: mongoose.ObjectId, ref: 'User'},
    status: getStatusType(userStatus, 'pending'),
    sessions: {type: mongoose.ObjectId, ref: 'Session'},
    authorizations: {type: mongoose.ObjectId, ref: 'Authorization'},
    factors: [
        require('./factor'),
    ],
}, commonSchema);

const userSchema = new mongoose.Schema(schema);

userSchema.virtual('password').set(async function (v) {
    this.password_hash = await scrypt.kdfSync(v, scryptParameters).toString('base64');
});
userSchema.methods.validatePassword = async function (v) {
    return await scrypt.verifyKdf(Buffer.from(this.password_hash, 'base64'), v);
};

userSchema.pre('save', async function () {
    if (!this.createdAt) {
        this.createdAt = new Date();
    }
    this.modifiedAt = new Date();
});

userSchema.virtual('factors_enabled').get(function () {
    return !this.factors;
});
userSchema.virtual('active').get(function () {
    return userRoles[this.status].active;
});

userSchema.virtual('perms').get(function () {
    return userRoles[this.status].perms;
});

module.exports = {
    roles: userRoles,
    schema: userSchema,
};
