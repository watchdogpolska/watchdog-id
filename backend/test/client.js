'use strict';
const ava = require('ava').default;
const {startServer, stopServer, asAdminUser, createFakeService, createFakeClient} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('client: create', asAdminUser(async t => {
    const service = {
        name: `test-service-${Math.random()}`,
        redirect_uri: [
            'https://endpoint/',
        ],
    };
    const resp = await t.context.api
        .post('v1/client')
        .send(service)
        .expect(200);
    t.true(!!resp.body._id);
    t.true(resp.body.name === service.name);
    t.true(!!resp.body.client_secret);
}));

ava('client: list', asAdminUser(async t => {
    const obj = await createFakeClient(t);
    const resp = await t.context.api.get('v1/client').expect(200);
    t.true(Array.isArray(resp.body));
    t.true(!!resp.body.find(x => x._id === obj._id));
}));

ava('service: et', asAdminUser(async t => {
    const service = await createFakeService(t);

    await t.context.api
        .get(`v1/service/${service._id}`)
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(!resp.body.client_secret);
        });
}));
