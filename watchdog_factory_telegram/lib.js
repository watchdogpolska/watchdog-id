'use strict';

const {badRequest} = require('boom');
const crypto = require('crypto');
const phoneUtil = require('google-libphonenumber').PhoneNumberUtil.getInstance();
const PhoneNumberType = require('google-libphonenumber').PhoneNumberType;
const PhoneNumberFormat = require('google-libphonenumber').PhoneNumberFormat;

const acceptedPhoneNumberType = [
    PhoneNumberType.MOBILE,
    PhoneNumberType.FIXED_LINE,
    PhoneNumberType.FIXED_LINE_OR_MOBILE,
];

const defaultPhoneCountry = 'PL';

const validatePhone = (phone) => {
    const number = phoneUtil.parse(phone, defaultPhoneCountry);
    if (!phoneUtil.isValidNumber(number)) {
        throw badRequest('The phone number entered is not valid.');
    }

    if (!acceptedPhoneNumberType.includes(phoneUtil.getNumberType(number))) {
        throw badRequest('The phone number entered is not valid. Only mobile phone or fixed line accepted.');
    }
    return true;
};

const formatPhone = (phone) => phoneUtil.format(phoneUtil.parse(phone, defaultPhoneCountry), PhoneNumberFormat.E164);

const getToken = (size = 48) => new Promise((resolve, reject) =>
    crypto.randomBytes(size, function (err, buffer) {
        if (err) {
            reject(err);
        }
        resolve(buffer.toString('hex'));
    })
);

module.exports = {
    getToken, validatePhone, formatPhone,
};
