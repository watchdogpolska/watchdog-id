'use strict';
const ava = require('ava').default;
const {startServer, stopServer, asAdminUser, createFakeService, generateWebKey} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('service: create', asAdminUser(async t => {
    const service = {
        title: `test-service-${Math.random()}`,
        description: 'example-description',
        endpointUrl: 'https://endpoint/',
        status: 'active',
        features: {
            passwordReset: false,
            userProvidedUsername: false,
        },
    };
    const resp = await t.context.api
        .post('v1/service')
        .send(service)
        .expect(200);
    t.true(!!resp.body._id);
    t.true(resp.body.title === service.title);
}));

ava('service: list', asAdminUser(async t => {
    const service = await createFakeService(t);
    const resp = await t.context.api.get('v1/service').expect(200);
    t.true(Array.isArray(resp.body));
    t.true(resp.body.find(x => x.title === service.title)._id === service._id);
}));

ava.todo('service: list for user');

ava('service: change key', asAdminUser(async t => {
    const service = await createFakeService(t);

    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({key: await generateWebKey()})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(!!resp.body.key);
        });
}));

ava('service: change notification address', asAdminUser(async t => {
    const service = await createFakeService(t);
    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({endpointUrl: 'http://httpbin.org/ip'})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(resp.body.endpointUrl === 'http://httpbin.org/ip');
        });
}));

ava('service: deactivate', asAdminUser(async t => {
    const service = await createFakeService(t);

    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({status: 'deactivated'})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(resp.body.status === 'deactivated');
        });
}));
