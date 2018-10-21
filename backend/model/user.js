'use strict';
const {EmailType}= require("./lib/types");

const {commonSchema} = require("./lib/common");
const {userStatus} = require("./lib/status");
const {getStatusType} = require("./lib/types");
const mongoose = require('mongoose');

const schema = Object.assign({
    username: {
        type: String,
        // unique: true,
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
    password: {
        type: String,
        required: true
    },
    status: getStatusType(userStatus)
}, commonSchema);

const userSchema = new mongoose.Schema(schema);

userSchema.pre('save', function(next) {
  if (!this.createdAt) {
      this.createdAt = new Date;
  }
  this.modifiedAt = new Date;
  next();
});

userSchema.virtual('active').get(function () {
    return ['accepted', 'admin'].includes(this.active)
});

module.exports = userSchema;
