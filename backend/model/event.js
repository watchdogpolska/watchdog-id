'use strict';
const mongoose = require('mongoose');
const {getStatusType} = require("./lib/types");
const {eventType} = require("./lib/status");

const schema = {
    userId: {
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    },
    status: getStatusType(eventType),
    createdAt: Date,
    modifiedAt: Date,
    data: {}
};
const eventSchema = new mongoose.Schema(schema);

eventSchema.pre('save', function(next) {
  if (!this.createdAt) {
      this.createdAt = new Date;
  }
  this.modifiedAt = new Date;
  next();
});

module.exports = eventSchema;
