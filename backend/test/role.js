'use strict';
const ava = require('ava').default;
const {startServer, stopServer, withAdminUser, createFakeUser, createFakeRole, createFakeService} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('utworzenie roli', withAdminUser(async (t, session) => {
    const body = {
        title: `test-role-${Math.random()}`,
        description: 'example-description',
        status: 'active',
    };
    const service = await createFakeService(t);
    return t.context.api.post(`v1/service/${service._id}/role`)
        .send(body)
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(resp.body.status === 'active');
            t.true(resp.body.manager === session.user);
        })
}));

ava('pobranie listy ról usługi', withAdminUser(async t => {
    const role = await createFakeRole(t);

    return t.context.api
        .get(`v1/service/${role.service._id}/role`)
        .expect(200)
        .then(resp => resp.body)
        .then(list => {
            t.true(list.some(x => x._id === role._id));
        })
}));

ava('zmiana nazwy roli', withAdminUser(async (t, session) => {
    const role = await createFakeRole(t);

    return t.context.api
        .post(`v1/service/${role.service._id}/role/${role._id}`)
        .send({title: 'extra-new-name'})
        .expect(200)
        .then(resp => resp.body)
        .then(new_role => {
            t.true(new_role.title === 'extra-new-name');
            t.true(new_role.manager === session.user);
        })
}));

ava('zmiana operatora roli i jej opisu', withAdminUser(async (t) => {
    const role = await createFakeRole(t);
    const extraUser = await createFakeUser(t, {
        username: `extra-user-${Math.random()}`,
    });
    return t.context.api
        .post(`v1/service/${role.service._id}/role/${role._id}`)
        .send({
            manager: extraUser._id,
            description: 'new-description',
        })
        .expect(200)
        .then(resp => resp.body)
        .then(new_role => {
            t.true(new_role.title === role.title);
            t.true(new_role.manager === extraUser._id);
            t.true(new_role.description === 'new-description');
        })
}));
