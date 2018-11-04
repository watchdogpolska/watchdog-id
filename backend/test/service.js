'use strict';
const ava = require('ava').default;
const {startServer, stopServer, withAdminUser, createFakeService, generateWebKey} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('utworzenie usługi', withAdminUser(async t => {
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

        await t.context.api
            .post('v1/service')
            .send(service)
            .expect(200)
            .then(resp => {
                t.true(!!resp.body._id);
                t.true(resp.body.title === service.title);
            })
    }
));

ava('pobranie listy usług systemu', withAdminUser(async t => {
    const service = await createFakeService(t);
    await t.context.api.get('v1/service').expect(200).then(resp => {
        t.true(Array.isArray(resp.body));
        t.true(resp.body.find(x => x.title === service.title)._id === service._id);
    });
}));

ava.todo('pobranie listy usług użytkownika');

ava('zmiana klucza usługi', withAdminUser(async t => {
    const service = await createFakeService(t);

    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({key: await generateWebKey()})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(!!resp.body.key);
        })
}));

ava('zmiana adresu powiadomień usługi', withAdminUser(async t => {
    const service = await createFakeService(t);
    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({endpointUrl: 'http://httpbin.org/ip'})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(resp.body.endpointUrl === 'http://httpbin.org/ip');
        })
}));

ava('deaktywacja usługi', withAdminUser(async t => {
    const service = await createFakeService(t);

    await t.context.api
        .post(`v1/service/${service._id}`)
        .send({status: 'deactivated'})
        .expect(200)
        .then(resp => {
            t.true(!!resp.body._id);
            t.true(resp.body.status === 'deactivated');
        })
}));
