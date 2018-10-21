'use strict';
const mongoose = require('mongoose');
const {opinionStatus} = require("./lib/status");
const {getStatusType} = require("./lib/types");
const {commonSchema }= require("./lib/common");

const opinionSchema = new mongoose.Schema(Object.assign({
    userId: {
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    },
    status: getStatusType(opinionStatus),
    commend: String
}, commonSchema));

opinionSchema.pre('save', function(next) {
  if (!this.createdAt) {
      this.createdAt = new Date;
  }
  this.modifiedAt = new Date;
  next();
});

module.exports = opinionSchema;
