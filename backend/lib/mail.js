'use strict';
const settings = require('../settings');
const Email = require('email-templates');
const nodemailer = require('nodemailer');

const transport = nodemailer.createTransport(settings.SMTP_URL);

const email = (options) => new Email(Object.assign({}, {
    message: {
        from: settings.DEFAULT_MAIL_FROM,
    },
    transport: transport,
}, options));

const opinionCreated = (user, opinion, service) => email().send({
    template: 'opinionCreated',
    message: {
        headers: {
            'X-Event-Type': 'opinionCreated',
        },
        to: user.email,
    },
    locals: {opinion, service},
});

const serviceCreated = (user, service) => email().send({
    message: {
        template: 'serviceCreated',
        headers: {
            'X-Event-Type': 'serviceCreated',
        },
        to: user.email,
    },
    locals: {service},
});

const roleCreated = (user, role, service) => email().send({
    template: 'roleCreated',
    message: {
        headers: {
            'X-Event-Type': 'roleCreated',
        },
        to: user.email,
    },
    locals: {role, service},
});

const userCreated = (user) => email().send({
    template: 'userCreated',
    message: {
        headers: {
            'X-Event-Type': 'userCreated',
        },
        to: user.email,
    },
    locals: {user},
});

const accessRequestCreated = (user, access_request) => email({
    headers: {
        'X-Event-Type': 'accessRequestCreated',
    },
}).send({
    template: 'accessRequestCreated',
    message: {
        headers: {
            'X-Event-Type': 'accessRequestCreated',
        },
        to: user.email,
    },
    locals: {access_request},
});

const accessRequestAccepted = (user, access_request) => email().send({
    template: 'accessRequestCreated',
    message: {
        headers: {
            'X-Event-Type': 'accessRequestAccepted',
        },
        to: user.email,
    },
    locals: {access_request},
});

module.exports = {
    opinionCreated,
    serviceCreated,
    roleCreated,
    userCreated,
    accessRequestCreated,
    accessRequestAccepted,
};
