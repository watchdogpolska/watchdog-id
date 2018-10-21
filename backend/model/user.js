'use strict';
const {EmailType}= require("./lib/types");

const {commonSchema} = require("./lib/common");
const {userStatus} = require("./lib/status");
const {getStatusType} = require("./lib/types");
const mongoose = require('mongoose');
const scrypt = require('scrypt');

const scryptParameters = scrypt.paramsSync(0.1);

const schema = Object.assign({
    username: {
        type: String,
        unique: true,
        required: true
    },
    email: EmailType,
    first_name: {
        type: String,
        required: true
    },
    second_name: {
        type: String,
        required: true
    },
    password_hash: {
        type: String,
        required: true,
        select: false
    },
    status: getStatusType(userStatus),
    sessions: { type: mongoose.ObjectId, ref: 'Session' },
}, commonSchema);

const userSchema = new mongoose.Schema(schema);

userSchema.virtual('password').set(async function(v) {
    this.password_hash = await scrypt.kdfSync(v, scryptParameters).toString('base64')
});
userSchema.methods.validatePassword = async function (v) {
    return await scrypt.verifyKdf(Buffer.from(this.password_hash, 'base64'), v);
};

userSchema.pre('save', async function(next) {
  if (!this.createdAt) {
      this.createdAt = new Date;
  }
  this.modifiedAt = new Date;
});

userSchema.virtual('active').get(function () {
    return ['accepted', 'admin'].includes(this.status)
});

module.exports = userSchema;
