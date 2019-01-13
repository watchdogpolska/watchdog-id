'use strict';
const u2f = require('u2f');
const {badRequest} = require('boom');

module.exports = settings => {
    const store = require('watchdog_factory_common').stateless_cookie('u2f_challenge', settings.JWT_SECRET);
    const APP_ID = settings.U2F_APP_ID || 'my-app-id';

    return {
    name: 'U2F',
    registrationChallengeHandler: async (user, factory_instance)  => {
        factory_instance.challenge = u2f.request(APP_ID);
    },
    registrationVerificationHandler: async (user, factory_instance, requestInput) => {
        const result = u2f.checkRegistration(factory_instance.challenge, requestInput.challenge);
        if (!result.successful) {
            throw badRequest(result.errorMessage, result);
        }
        factory_instance.challenge = {};
        factory_instance.config  = {
            publicKey: result.publicKey,
            keyHandle: result.keyHandle,
        };
    },
    authenticationChallengeHandler: async (user, factory_instance) => {
        const authRequest = u2f.request(APP_ID, factory_instance.config.keyHandle);
        const cookie = await store.genCookie(user, authRequest);
        return {
            cookie, authRequest,
        };
    },
    authenticationVerificationHandler: async (user, factory_instance, requestInput) => {
        const publicKey = factory_instance.config.publicKey;
        const authRequest = await store.readCookie(user, requestInput.cookie);
        const result = u2f.checkSignature(authRequest, requestInput.challenge, publicKey);
        if (!result.successful) {
            throw badRequest(result.errorMessage, result);
        }
        return true;
    },
}}
