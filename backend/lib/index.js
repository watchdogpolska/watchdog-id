'use strict';
const {unauthorized} = require('boom');

// const pluginInterface = () => ({
//     name: 'unknown name',
//     registrationChallengeHandler: async (user, factor, requestInput) => {
//     },
//     registrationVerificationHandler: async (user, factor, requestInput) => {
//     },
//     authenticationChallengeHandler: async (user, factor, requestInput) => {
//          {}
//     },
//     authenticationVerificationHandler: async (user, factor, requestInput) => {
//          {}
//     },
// });

const HEADER = 'X-Watchdog-OTP';

const factors = [];

module.exports = {
    use: async (module) => factors.push(await module()),
    getAll: () => factors,
    getNames: () => factors.map(x => x.name),
    enforceFactorRequest: async ctx => {
        if (!ctx.state.user || !ctx.state.user.factors_enabled) {
            return;
        }
        if (!ctx.request.headers[HEADER.toLowerCase()]) {
            ctx.headers[HEADER.toLowerCase()] = 'required';
            throw unauthorized(`Two-factor authentication of the request is required. Use '${HEADER}' header.`, ctx.state.user.factors);
        }
        const otpHeader = ctx.request.headers[HEADER.toLowerCase()];
        const matchChallenge = otpHeader.match(/^(.+?)\s*=\s*(.+?)\s*$/);
        if (matchChallenge.length !== 3) {
            throw unauthorized(`Unable to parse header '${HEADER}'`, ctx.state.user.factors);
        }
        const factorId = matchChallenge[1];
        const factorValue = matchChallenge[2];
        const factor = ctx.state.user.factors.id(factorId);
        if (!factor) {
            throw unauthorized('The factor ID required is not valid.', ctx.state.user.factors);
        }
        const factoryModule = factors.find(x => x.name === factor.name);

        if (!factoryModule) {
            throw unauthorized('The factor method is no longer valid.', ctx.state.user.factors);
        }

        if (factorValue === 'required') {
            ctx.status = 401;
            ctx.headers[HEADER.toLowerCase()] = `${factor._id.toString()}=required`;
            await factoryModule.authenticationChallengeHandler(ctx, factor.data);
        } else {
            await factoryModule.authenticationVerificationHandler(ctx, factor.data);
        }
    },
};
