'use strict';
const jwt = require('jsonwebtoken');
const promisify = require('util').promisify;
const sign = promisify(jwt.sign);
const verify = promisify(jwt.verify);

const CookieStore = (store_name, secret) => {
    const genCookie = (user, data) => {
        const claim = Object.assign({}, data, {
            sub: user._id,
            aud: store_name,
        });
        return sign(claim, secret);
    };

    const readCookie = (user, data) => verify(data, secret, {
        sub: user._id,
        audience: store_name,
    });
    return {genCookie, readCookie};
};

module.exports = CookieStore;
