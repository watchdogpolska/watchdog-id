'use strict';
const nodemailer = require('nodemailer');
const settings = require('../settings');

const transporter = nodemailer.createTransport(settings.SMTP_URL);

const opinionCreated = (ctx, obj) => new Promise((resolve, reject) => {

});

const userCreated = (ctx, obj) => new Promise((resolve, reject) => {
});

const serviceCreated = (ctx, obj) => new Promise((resolve, reject) => {

});

const connect = signals => {
    signals.connect(opinionCreated, 'opinionCreated');
    signals.connect(userCreated, 'userCreated');
    signals.connect(serviceCreated, 'serviceCreated');
};

module.exports = {
    connect,
};
