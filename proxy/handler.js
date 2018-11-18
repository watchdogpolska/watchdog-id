const jwt = require('jsonwebtoken');
const {pem2jwk} = require('pem-jwk');
const options = require('./options');
const passport = require('passport');
const proxy = require('./proxy');

const login_required = (authenticated, login_enforce) => (req, res) => {
    if (req.user) {
        return authenticated(req, res);
    }
    return login_enforce(req, res);
};

const enforce_login = (req, res) => {
    const state = jwt.sign({
        sub: req.url,
        aud: options.SERVICE_NAME,
        iss: options.SERVICE_NAME,
    }, options.PRIVATE_KEY, options.JWT);
    return passport.authenticate('google', {
        ...options.AUTH,
        state
    })(req, res);
};

const secure_zone = login_required(proxy.handler, enforce_login);

const callback = function (req, res) {
    if (req.query.state) {
        const state = req.query.state;
        try {
            const decoded = jwt.verify(state, options.PUBLIC_KEY, {
                aud: options.SERVICE_NAME,
                iss: options.SERVICE_NAME,
            });
            return res.redirect(decoded.sub);
        } catch (err) {
            res.sendStatus(500);
        }
    }
    res.redirect('/');
};

const failed = (req, res) => res
    .sendStatus(500)
    .send('The process was unsuccessful. Please try again later or contact the administrator!');

const jwk = (req, res) => res.send(pem2jwk(options.PUBLIC_KEY));

module.exports = {
    secure_zone,
    callback,
    jwk,
    failed
};
