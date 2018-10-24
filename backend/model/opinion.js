'use strict';
const mongoose = require('mongoose');
const {opinionStatus} = require('./lib/status');
const {getStatusType} = require('./lib/types');
const {commonSchema }= require('./lib/common');

const opinionSchema = new mongoose.Schema(Object.assign({
    userId: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
    },
    status: getStatusType(opinionStatus),
    commend: String,
}, commonSchema));


module.exports = opinionSchema;
