'use strict';
const {isEmail} = require('validator');

const getStatusType = status => ({type: String, enum: status, required: true});

const EmailType = {
    type: String,
    validate: [isEmail, 'Please fill a valid email address'],
    required: true,
};

module.exports = {
    getStatusType,
    EmailType,
};
