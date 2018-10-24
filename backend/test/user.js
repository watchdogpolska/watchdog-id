const ava = require('ava').default;
const {startServer, stopServer, withFakeUser, withSession} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);
ava.beforeEach(withFakeUser);


ava.serial('GET /user as authenticated', withSession(async (t, session) => {
    await t.context.api
        .get(`v1/user/${session.user}`)
        .expect(200)
        .then(resp => {
            t.true(resp.body._id === session.user)
        })
}));

ava.serial('make user suspended', withSession(async (t, session) => {
    await t.context.api
        .del(`v1/user/${session.user}`)
        .expect(200)
        .then(resp => {
            t.true(resp.body.status === 'suspended')
        })
}));
