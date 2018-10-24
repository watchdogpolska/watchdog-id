const ava = require('ava').default;
const {startServer, stopServer, withFakeUser, withFakeService, createUser, withRole, withFakeRole} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava.beforeEach(withFakeUser);
ava.beforeEach(withFakeService);
ava.beforeEach(withFakeRole);


ava('utworzenie roli', withRole(async (t, session, service, role) => {
    t.true(!!role._id);
    t.true(role.status === 'active');
    t.true(role.manager === session.user);
}));

ava('pobranie listy ról usługi', withRole(async (t, session, service, role) => t.context.api
    .get(`v1/service/${service._id}/role`)
    .expect(200)
    .then(resp => resp.body)
    .then(list => {
        t.true(list.some(x => x._id === role._id))
    })
));

ava('zmiana nazwy roli', withRole(async (t, session, service, role) => t.context.api
    .post(`v1/service/${service._id}/role/${role._id}`)
    .send({'title': 'extra-new-name'})
    .expect(200)
    .then(resp => resp.body)
    .then(new_role => {
        t.true(new_role.title === 'extra-new-name');
        t.true(new_role.manager === session.user)
    })
));

ava('zmiana operatora roli i jej opisu', withRole(async (t, session, service, role) =>
    createUser(t, Object.assign(t.context.fakeUser, {
        username: `extra-user-${Math.random()}`
    })).then(extraUser => t.context.api
        .post(`v1/service/${service._id}/role/${role._id}`)
        .send({
            'manager': extraUser._id,
            'description': 'new-description'
        })
        .expect(200)
        .then(resp => resp.body)
        .then(new_role => {
            t.true(new_role.title === t.context.fakeRole.title);
            t.true(new_role.manager === extraUser._id);
            t.true(new_role.description === 'new-description')
        })
    )
));
