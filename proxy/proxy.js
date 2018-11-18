const httpProxy = require('http-proxy');
const {cookieEncode} = require('./utils');
const cookie = require('cookie');
const options = require('./options');
const jwt = require('jsonwebtoken');

const proxy = httpProxy.createProxyServer({ws: false, xfwd: true});

proxy.on('proxyReq', (proxyReq, req) => {
    const user_cookie = cookie.parse(req.headers.cookie || {});
    delete user_cookie[options.COOKIE_NAME];
    proxyReq.setHeader('Cookie', cookieEncode(user_cookie));
    proxyReq.setHeader('x-watchdog-authenticated-user-id', req.user.userId);
    proxyReq.setHeader('x-watchdog-authenticated-user-email', req.user.email);
    proxyReq.setHeader('REMOTE_USER', req.user.email);
    const assertion = jwt.sign({
        sub: req.user.email,
        aud: new URL(options.TARGET_URL).hostname,
        iss: options.SERVICE_NAME,
    }, options.PRIVATE_KEY, options.JWT);
    proxyReq.setHeader('x-watchdog-jwt-assertion', assertion);
});

const handler = (req, res) => proxy.web(req, res, {
    target: options.TARGET_URL,
}, (err) => {
    console.log(err);
    res.send("Connection to the internal server failed.");
});

module.exports = {
    proxy,
    handler
};
