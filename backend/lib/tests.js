'use strict';
const request = require('supertest');
const mongoose = require('mongoose');
const JSONWebKey = require('json-web-key');
const {promisify} = require('util');
const forge = require('node-forge');

const api = (options) => {
    const agent = request.agent(`http://${options.host}:${options.port}/`);
    agent.login = (username, password) => agent
        .post(`v1/user/${username}/session`)
        .send({password})
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

const createFakeUser = (t, body = {}) => {
    const user = Object.assign({
        username: `string-${Math.random()}`,
        first_name: 'string',
        second_name: 'string',
        password: 'string',
        status: 'pending',
        email: 'user@example.com',
    }, body);
    return t.context.api.post('v1/user')
        .send(user)
        .expect(200)
        .then(resp => resp.body);
};

const withSession = (status = 'accepted', fn) => async t => {
    const user = await createFakeUser(t, {password: 'pass'});
    const User = mongoose.model('User');
    await User.findOneAndUpdate({_id: user._id}, {
        status: status,
    });
    const session = await t.context.api.login(user.username, 'pass');
    await fn(t, session);
};

const withAdminUser = fn => withSession('admin', fn);

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


const withRole = fn => async (t, session) => {
    const service = await createFakeService(t);
    const role = await createFakeRole(t);
    await fn(t, session, service, role)
};

const createFakeRole = async (t, body = {}) => {
    const role = Object.assign({
        title: `test-role-${Math.random()}`,
        description: 'example-description',
        status: 'active',
    }, body);
    const service = await createFakeService(t);
    return t.context.api.post(`v1/service/${service._id}/role`)
        .send(role)
        .expect(200)
        .then(resp => Object.assign(resp.body, {
            service: service
        }));
};

module.exports = {
    api,
    startServer,
    stopServer,
    withAdminUser,
    withSession,
    generateWebKey,
    withRole,
    createFakeUser,
    createFakeRole,
    createFakeService
};
