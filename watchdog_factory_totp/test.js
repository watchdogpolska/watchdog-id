'use strict';
const ava = require('ava').default;
const otplib = require('otplib');
const factorTest = require('watchdog_factory_common').tests;

const secret = 'xxx';

ava('test TOTP flow', factorTest.genericFactorTest({
    getFactor: () => require('.')(),
    registration: {
        verification: () => ({
            challenge: otplib.authenticator.generate(secret),
            secret,
        }),
    },
    authentication: {
        verification: () => ({
            challenge: otplib.authenticator.generate(secret),
        }),
    },
}));
