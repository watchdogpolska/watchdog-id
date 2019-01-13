'use strict';
const {badRequest} = require('boom');
const otplib = require('otplib');
const lib = require('./lib');
const aws = require('./aws');

module.exports = async (settings, options = {}) => {
    const skipSms = options.skipSms || true;
    const instanceSecret = await lib.getToken();
    const sendSms = (phone, token) => aws.sendSms(phone, token) ? skipSms : {send: true};

    const getSecret = phone => `${instanceSecret}:${phone}`;
    const getToken = phone => otplib.authenticator.generate(getSecret(phone));

    return {
        name: 'SMS',
        registrationChallengeHandler: async (user, factory_instance, requestInput={}) => {
            lib.validatePhone(requestInput.phone);
            const phone = lib.formatPhone(requestInput.phone);
            const token = getToken(phone);
            console.log({token, phone});
            await sendSms(requestInput.phone, token);
            factory_instance.config = {
                phone,
            };
        },
        registrationVerificationHandler: async (user, factory_instance, requestInput={}) => {
            const secret = getSecret(factory_instance.config.phone);
            console.log({expectedToken: getToken(factory_instance.config.phone)});
            console.log({factory_instance, requestInput});
            if (!otplib.authenticator.check(requestInput.challenge, secret)) {
                throw badRequest('Invalid one-time SMS code for registration. Try again later.');
            }
        },
        authenticationChallengeHandler: async (user, factory_instance) => {
            const token = getToken(factory_instance.config.phone);
            await sendSms(factory_instance.config.phone, token);
        },
        authenticationVerificationHandler: async (user, factory_instance, requestInput={}) => {
            const secret = getSecret(factory_instance.config.phone);
            if (!otplib.authenticator.check(requestInput.challenge, secret)) {
                throw badRequest('Invalid one-time SMS code for authentication. Try again later.');
            }
            return true;
        },
        getToken,
    };
};
