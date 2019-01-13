'use strict';
const {badRequest} = require('boom');
const yub = require('yub');

const verify = (y, otp, allowReply = false) => new Promise((resolve, reject) => {
    y.verify(otp, (err, data) => {
        if (err) return reject(err);
        if (data.status === 'REPLAYED_OTP' && allowReply) return resolve(data);
        if (data.status !== 'OK') return reject(data);
        return resolve(data);
    });
});

module.exports = async (settings, options = {}) => {
    const allowReply = options.allowReply || false;
    const y = new yub(settings.YUBICO_CLIENT_ID, settings.YUBICO_SECRET_KEY);

    return {
        name: 'YubicoOTP',
        registrationChallengeHandler: async (user, factory_instance, requestInput) => {
            let data;
            try {
                data = await verify(y, requestInput.challenge, allowReply);
            } catch (err) {
                throw badRequest('Invalid one-time Yubico code for registration. Try again later.', err);
            }
            factory_instance.config = {
                identity: data.identity,
            };
        },
        authenticationVerificationHandler: async (user, factory_instance, requestInput) => {
            let data;
            try {
                data = await verify(y, requestInput.challenge, allowReply);
            } catch (err) {
                throw badRequest('Invalid one-time Yubico code for authentication. Try again later.', err);
            }
            if (data.identity !== factory_instance.config.identity) {
                throw badRequest('Mismatch one-time Yubico code. Try use other token.');
            }
            return true;
        },
    };
};
