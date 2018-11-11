'use strict';
const request = require('supertest');
const mongoose = require('mongoose');
const JSONWebKey = require('json-web-key');
const {promisify} = require('util');
const forge = require('node-forge');
const mockery = require('mockery');
const nodemailerMock = require('nodemailer-mock');

const api = (options) => {
    const agent = request.agent(`http://${options.host}:${options.port}/`);
    agent.login = (username, password) => agent
        .post(`v1/user/me/session`)
        .send({username, password})
        .expect(200)
        .then(resp => resp.body);
    return agent;
};

const startServer = async t => {
    const port = Math.round(Math.random() * 10000 + 2000);
    t.context.server = await require('../index')({LISTEN_PORT: port});
    t.context.api = api({
        host: 'localhost',
        port,
    });
};

const stopServer = t => new Promise((resolve, reject) => {
    t.context.server.once('close', resolve);
    t.context.server.once('error', reject);
    t.context.server.close();
});

const createFakeUser = async (t, body = {}) => {
    const user = Object.assign({
        username: `string-${Math.random()}`,
        first_name: 'string',
        second_name: 'string',
        password: 'string',
        status: 'pending',
        email: 'user@example.com',
    }, body);
    let resp = await t.context.api.post('v1/user')
        .send(user)
        .expect(200);
    if (body.manager) {
        const User = mongoose.model('User');
        await User.findOneAndUpdate({_id: resp.body._id}, {
            manager: body.manager,
        });
        resp = await t.context.api.get(`v1/user/${resp.body._id}`);
    }
    if (body.status){
        const User = mongoose.model('User');
        await User.findOneAndUpdate({_id: resp.body._id}, {
            status: body.status,
        });
        resp.body.status = body.status
    }
    return resp.body;
};

const withSession = (status = 'accepted', fn) => async t => {
    const user = await createFakeUser(t, {
        password: 'pass'
    });
    const User = mongoose.model('User');
    await User.findOneAndUpdate({_id: user._id}, {
        status: status,
    });
    const session = await t.context.api.login(user.username, 'pass');
    await fn(t, session);
};

const asAdminUser = fn => withSession('admin', fn);

const generateWebKey = async () => {
    const keySet = await promisify(forge.rsa.generateKeyPair)({
        bits: 128,
        e: 0x10001,
    });
    const pem = forge.pki.publicKeyToPem(keySet.publicKey);
    return JSONWebKey.fromPEM(pem);
};

const createFakeService = (t, body = {}) => {
    const user = Object.assign({
        title: `test-service-${Math.random()}`,
        description: 'example-description',
        endpointUrl: 'https://endpoint/',
        status: 'active',
        features: {
            passwordReset: false,
            userProvidedUsername: false,
        },
    }, body);
    return t.context.api.post('v1/service')
        .send(user)
        .expect(200)
        .then(resp => resp.body);
};


const createFakeRole = async (t, body = {}) => {
    let serviceId = body.service;
    if(!serviceId ){
        serviceId = (await createFakeService(t))._id;
    }
    const role = Object.assign({
        title: `test-role-${Math.random()}`,
        description: 'example-description',
        status: 'active',
        serviceId: serviceId
    }, body);
    return t.context.api.post(`v1/role`)
        .send(role)
        .expect(200)
        .then(resp => resp.body);
};

const createFakeAccessRequest = async (t, body = {}) => {
    let usersId = body.usersId;
    if (!usersId) {
        usersId = [(await createFakeUser(t))._id];
    }
    let rolesId = body.rolesId;
    if (!rolesId) {
        const role = await createFakeRole(t);
        rolesId = [role._id];
    }

    const user = Object.assign({
        comment: `test-access-request-${Math.random()}`,
        usersId: usersId,
        rolesId: rolesId,
    }, body);
    return t.context.api.post('v1/access_request')
        .send(user)
        .expect(200)
        .then(resp => resp.body);
};

const avaMockNodeMailer = (ava) => {
    ava.beforeEach(() => {
        mockery.enable({
            warnOnUnregistered: false,
        });
        mockery.registerMock('nodemailer', nodemailerMock);
    });
    ava.afterEach(() => {
        nodemailerMock.mock.reset();
    });
    ava.after(() => {
        mockery.deregisterAll();
        mockery.disable();
    });
    return nodemailerMock;
};

module.exports = {
    api,
    avaMockNodeMailer,
    startServer,
    stopServer,
    asAdminUser,
    withSession,
    generateWebKey,
    createFakeUser,
    createFakeRole,
    createFakeService,
    createFakeAccessRequest,
};
