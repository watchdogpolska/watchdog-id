'use strict';
const mongoose = require('mongoose');
const {opinionStatus} = require('../lib/model/status');
const {getStatusType} = require('../lib/model/types');
const {commonSchema }= require('../lib/model/common');

const opinionSchema = new mongoose.Schema(Object.assign({
    userId: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
    },
    status: getStatusType(opinionStatus),
    commend: String,
}, commonSchema));


module.exports = opinionSchema;
