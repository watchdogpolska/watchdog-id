'use strict';
const ava = require('ava').default;
const factorTest = require('watchdog_factory_common').tests;
const VirtualToken = require('virtual-u2f');
const token = new VirtualToken();


ava('test U2F flow', factorTest.genericFactorTest({
    getFactor: () => require('.')({JWT_SECRET: 'x'}),
    registration: {
        challenge: () => { },
        verification: async (factor, factory_instance) => ({
            challenge: await token.HandleRefCodeRegisterRequest(factory_instance.challenge),
            cookie: factory_instance.challenge.cookie,
        }),
    },
    authentication: {
        challenge: () => { },
        verification: async (factor, challenge, factory_instance) => ({
            challenge: await token.HandleRefCodeSignRequest(challenge.authRequest),
            cookie: challenge.cookie,
        }),
    },
}));

