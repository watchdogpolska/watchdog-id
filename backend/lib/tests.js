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
        host: "localhost",
        port
    });
};

const stopServer = t => new Promise((resolve, reject) => {
    t.context.server.once('close', resolve);
    t.context.server.once('error', reject);
    t.context.server.close();
});

const withFakeUser = t => {
    const no = Math.round(Math.random() * 10000 + 2000);
    t.context.fakeUser = {
        "username": `string-${no}`,
        "first_name": "string",
        "second_name": "string",
        "password": "string",
        "status": "pending",
        "email": 'user@example.com',
    };
};

const createUser = (t, body) => t.context.api.post('v1/user')
    .send(body)
    .expect(200)
    .then(resp => resp.body);

const withSession = fn => async t => {
    await t.context.api.post('v1/user').send(t.context.fakeUser);
    const session = await t.context.api.login(
        t.context.fakeUser.username,
        t.context.fakeUser.password
    );
    await fn(t, session)
};

const withAdminUser = fn => withSession(async (t, session) => {
    const model = require('./../model');
    await mongoose.model('User', model.userSchema);
    const User = mongoose.model('User');
    await User.findOneAndUpdate({_id: session.user}, {
        status: 'admin'
    });
    await fn(t, session)
});


const withService = fn => withAdminUser((t, session) => t.context.api
    .post('v1/service').send(t.context.fakeService)
    .expect(200)
    .then(resp => resp.body)
    .then(async service => {
        await fn(t, session, service)
    })
);
const generateWebKey = async () => {
    const keySet = await promisify(forge.rsa.generateKeyPair)({
        bits: 128,
        e: 0x10001
    });
    const pem = forge.pki.publicKeyToPem(keySet.publicKey);
    return JSONWebKey.fromPEM(pem);
};

const withFakeService = t => {
    t.context.fakeService = {
        title: `test-service-${Math.random()}`,
        description: 'example-description',
        endpointUrl: 'https://endpoint/',
        status: 'active',
        features: {
            passwordReset: false,
            userProvidedUsername: false
        }
    }
};

const withRole = fn => withService((t, session, service) => t.context.api
    .post(`v1/service/${service._id}/role`)
    .send(Object.assign({}, t.context.fakeRole, {
        manager: session.user
    }))
    .expect(200)
    .then(resp => resp.body)
    .then(role => fn(t, session, service, role))
);

const withFakeRole = t => {
    t.context.fakeRole = {
        title: `test-role-${Math.random()}`,
        description: 'example-description',
        status: 'active',
    }
};

module.exports = {
    api,
    startServer,
    stopServer,
    withFakeUser,
    withAdminUser,
    withSession,
    withService,
    generateWebKey,
    withFakeService,
    withRole,
    createUser,
    withFakeRole
};
