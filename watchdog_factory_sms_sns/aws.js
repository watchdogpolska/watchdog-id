'use strict';
const AWS = require('aws-sdk');

const sns = new AWS.SNS({region: 'us-east-1', apiVersion: '2010-03-31'});

const sendSms = (phone, code) => sns.publish({
    Message: code,
    PhoneNumber: phone,
}).promise();

module.exports = {sendSms};
