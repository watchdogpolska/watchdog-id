const ava = require('ava').default;
const {startServer, stopServer, withFakeUser, withAdminUser, withService, withFakeService, generateWebKey} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);
ava.beforeEach(withFakeUser);
ava.beforeEach(withFakeService);

ava('utworzenie usługi', withAdminUser(async t => t.context.api
    .post('v1/service')
    .send(t.context.fakeService)
    .expect(200)
    .then(resp => {
        t.true(!!resp.body._id);
        t.true(resp.body.title === t.context.fakeService.title)
    })
));

ava('pobranie listy usług systemu', withService(async (t, session, service) => {
    await t.context.api.get('v1/service').expect(200).then(resp => {
        t.true(Array.isArray(resp.body));
        t.true(resp.body.some(x => x.title === t.context.fakeService.title));
        t.true(resp.body.some(x => x._id === service._id))
    })
}));

ava.todo('pobranie listy usług użytkownika');

ava('zmiana klucza usługi', withService(async (t, session, service) => t.context.api
    .post(`v1/service/${service._id}`)
    .send({key: await generateWebKey()})
    .expect(200)
    .then(resp => {
        t.true(!!resp.body._id);
        t.true(!!resp.body.key);
    })
));

ava('zmiana adresu powiadomień usługi', withService(async (t, session, service) => t.context.api
    .post(`v1/service/${service._id}`)
    .send({endpointUrl: 'http://httpbin.org/ip'})
    .expect(200)
    .then(resp => {
        t.true(!!resp.body._id);
        t.true(resp.body.endpointUrl === 'http://httpbin.org/ip');
    })
));

ava('deaktywacja usługi', withService(async (t, session, service) => t.context.api
    .post(`v1/service/${service._id}`)
    .send({status: 'deactivated'})
    .expect(200)
    .then(resp => {
        t.true(!!resp.body._id);
        t.true(resp.body.status=== 'deactivated');
    })
));
