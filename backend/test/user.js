'use strict';
const ava = require('ava').default;
const {startServer, stopServer, withSession, createFakeUser} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);


ava('rejestracja', async t => {
    const username = `user-${Math.random()}`;

    await t.context.api
        .post('v1/user')
        .send({
            first_name: 'John',
            second_name: 'Smith',
            username: username,
            password: 'x',
            email: 'test@example.com',
        })
        .expect(200)
        .then(resp => {
            t.true(!!resp.body);
            t.true(resp.body.username === username);
            t.true(resp.body.first_name === 'John');
            t.true(resp.body.second_name === 'Smith');
            t.true(resp.body.email === 'test@example.com');
            t.true(resp.body.username === username);
            t.true(resp.body.status === 'pending');
            t.true(!resp.password_hash);
        });
});
ava("can not login on 'pending' user", async t => {
    const cred = {
        username: 'some-username',
        password: 'pass',
    };
    const user = await createFakeUser(t, cred);
    t.true(user.status === 'pending');

    await t.context.api
        .post(`v1/user/${cred.username}/session`)
        .send({password: cred.password})
        .expect(401)
        .then(resp => {
            t.true(!!resp.body);
        });
});
ava.todo('logowanie');
ava.todo('zmiana przełożonego');
ava.todo('zmiana imienia lub nazwiska');
ava.todo('zmiana hasła');

ava('GET /user as authenticated', withSession('accepted', async (t, session) => {
    await t.context.api
        .get(`v1/user/${session.user}`)
        .expect(200)
        .then(resp => {
            t.true(resp.body._id === session.user);
        });
}));

ava('make user suspended', withSession('accepted', async (t, session) => {
    await t.context.api
        .del(`v1/user/${session.user}`)
        .expect(200)
        .then(resp => {
            t.true(resp.body.status === 'suspended');
        });
}));


