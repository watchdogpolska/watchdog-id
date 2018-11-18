
const session = require("express-session");
const bodyParser = require("body-parser");
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const passport = require('passport');
const express = require('express');
const morgan = require('morgan');
const options = require('./options');
const handler = require('./handler');

passport.use(new GoogleStrategy(options.GOOGLE,
    function (accessToken, refreshToken, profile, cb) {
        if (options.GOOGLE.hostedDomain && options.GOOGLE.hostedDomain !== profile._json.hd) {
            return cb("Invalid domain. This service is not for you.")
        }
        const google_user = {
            token: accessToken,
            userId: profile._json.sub,
            email: profile._json.email,
            profile: profile._json
        };
        return cb(null, google_user);
    }
));

passport.serializeUser(function (user, done) {
    done(null, JSON.stringify(user));
});

passport.deserializeUser(function (user, done) {
    done(null, JSON.parse(user));
});

const session_options = {
    secret: options.SESSION_SECRET,
    cookie_name: options.COOKIE_NAME,
    resave: false,
    saveUninitialized: false
}

const app = express();

app.use(morgan('common'));
app.use(session(session_options));
app.use(bodyParser.urlencoded({extended: false}));
app.use(passport.initialize());
app.use(passport.session());
app.get('/auth_failed', handler.failed);
app.get('/auth_callback', passport.authenticate('google', options.AUTH), handler.callback);
app.get('/auth_keys', handler.jwk);
app.use(handler.secure_zone);

app.listen(5050);
