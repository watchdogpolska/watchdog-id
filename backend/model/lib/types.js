'use strict';
const {isEmail} = require('validator');

const getStatusType = (status, defaultValue) => {
    if(defaultValue){
        return {type: String, enum: status, default: defaultValue};
    }
    return {type: String, enum: status, required: true}
};

const EmailType = {
    type: String,
    validate: [isEmail, 'Please fill a valid email address'],
    required: true,
};

module.exports = {
    getStatusType,
    EmailType,
};
