'use strict';
const {getStatusType} = require("./lib/types");

const {accessRequestStatus}= require("./lib/status");
const {commonSchema }= require("./lib/common");
const eventSchema = require('./event');
const opinionSchema = require('./opinion');
const mongoose = require('mongoose');


const schema = Object.assign({
    comment: String,
    opinions: [opinionSchema],
    events: [eventSchema],
    usersId: [{
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    }],
    rolesId: [{
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    }],
    status: getStatusType(accessRequestStatus)
}, commonSchema);

const accessRequestSchema = new mongoose.Schema(schema);

accessRequestSchema.pre('save', function(next) {
  if (!this.createdAt) {
      this.createdAt = new Date;
  }
  this.modifiedAt = new Date;
  next();
});

module.exports = accessRequestSchema;
