'use strict';
const ava = require('ava').default;
const factorTest = require('watchdog_factory_common').tests;

const phone = '+48509992768';

ava('test SMS flow', factorTest.genericFactorTest({
    getFactor: () => require('.')({JWT_SECRET: 'xxxx'}, {skipSms: true}),
    registration: {
        challenge: () => ({
            phone,
        }),
        verification: (factor, factory_instance) => ({
            challenge: factor.getToken(factory_instance.config.phone),
        }),
    },
    authentication: {
        challenge: () => {},
        verification: (factor, challenge, factory_instance) => ({
            challenge: factor.getToken(factory_instance.config.phone),
        }),
    },
}));
