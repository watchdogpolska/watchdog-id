'use stricts';
const fs = require('fs');
module.exports = {
    SERVICE_NAME: 'watchdog_id',
    GOOGLE_HD: 'siecobywatelska.pl',
    SESSION_SECRET: 'xxxx',
    COOKIE_NAME: 'watchdog_id.sid',
    TARGET_URL: 'http://localhost:9000',
    PUBLIC_KEY: fs.readFileSync('rsa_public.key'),
    PRIVATE_KEY: fs.readFileSync('rsa_private.key'),
    JWT: {algorithm: 'RS256', expiresIn: '5m'},
    AUTH: {
        scope: ['openid profile email'],
        callbackURL: "http://watchdog.127.0.0.1.xip.io:5050/auth_callback",
        failureRedirect: '/auth_failed',
    },
    GOOGLE: {
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: "http://watchdog.127.0.0.1.xip.io:5050/auth_callback",
        userProfileURL: 'https://www.googleapis.com/oauth2/v3/userinfo',
        hostedDomain: 'siecobywatelska.pl'
    }
};
