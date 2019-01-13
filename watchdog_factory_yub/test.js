'use strict';
const ava = require('ava').default;
const factorTest = require('watchdog_factory_common').tests;

const yub_challenge = 'ccccccgnbkbinnjnvnvlieegebntgljhfhdbcgckkuli';

ava('test Yubico OTP flow', factorTest.genericFactorTest({
    getFactor: () => require('.')({}, {allowReply: true}),
    registration: {
        verification: () => ({challenge: yub_challenge}),
    },
    authentication: {
        verification: () => ({challenge: yub_challenge}),
    },
}));
