'use strict';
const ava = require('ava').default;
const {startServer, stopServer, asAdminUser, createFakeUser, createFakeRole, createFakeService} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('role: create', asAdminUser(async (t, session) => {
    const service = await createFakeService(t);
    const body = {
        title: `test-role-${Math.random()}`,
        description: 'example-description',
        status: 'active',
        serviceId: service._id,
    };
    const resp = await t.context.api.post('v1/role')
        .send(body)
        .expect(200);

    t.true(!!resp.body._id);

    t.true(resp.body.status === 'active');
    t.true(resp.body.manager === session.user);
}));

ava('role: list', asAdminUser(async t => {
    const role = await createFakeRole(t);

    const resp = await  t.context.api
        .get('v1/role')
        .expect(200)
        .then(resp => resp.body);

    t.true(resp.some(x => x._id === role._id));
}));

ava('role: rename', asAdminUser(async (t, session) => {
    const role = await createFakeRole(t);

    const resp = await  t.context.api
        .post(`v1/role/${role._id}`)
        .send({title: 'extra-new-name'})
        .expect(200)
        .then(resp => resp.body);
    t.true(resp.title === 'extra-new-name');
    t.true(resp.manager === session.user);
}));

ava('role: operator change & description update', asAdminUser(async (t) => {
    const role = await createFakeRole(t);
    const extraUser = await createFakeUser(t, {
        username: `extra-user-${Math.random()}`,
    });
    const resp = await t.context.api
        .post(`v1/role/${role._id}`)
        .send({
            manager: extraUser._id,
            description: 'new-description',
        })
        .expect(200)
        .then(resp => resp.body);
    t.true(resp.title === role.title);
    t.true(resp.manager === extraUser._id);
    t.true(resp.description === 'new-description');
}));
