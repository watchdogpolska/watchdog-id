'use strict';
const {badRequest} = require('boom');
const otplib = require('otplib');

module.exports = async () => ({
    name: 'TOTP',
    registrationVerificationHandler: async (user, factory_instance, requestInput) => {
        if (!otplib.authenticator.check(requestInput.challenge, requestInput.secret)) {
            throw badRequest('Invalid one-time TOTP code. Try again later.');
        }
        factory_instance.config = {
            secret: requestInput.secret
        };
    },
    authenticationVerificationHandler: async (user, factory_instance, requestInput) => {
        if (!otplib.authenticator.check(requestInput.challenge, factory_instance.config.secret)) {
            throw badRequest('Invalid one-time TOTP code. Try again later.');
        }
        return true;
    },
});
