'use strict';
const ava = require('ava').default;
const {startServer, stopServer, createFakeUser} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('authorization: create using basic authentication', async t => {
    const password = 'pass';

    const user = await createFakeUser(t, {
        password,
        status: 'accepted',
    });

    const authorization_resp = await t.context.api
        .post('v1/authorization')
        .auth(user.username, password)
        .expect(200)
        .then(resp => resp.body);

    const access_token = authorization_resp.access_token.token;
    const user_resp = await t.context.api
        .get('v1/user/me')
        .set('Authorization', `Bearer ${access_token}`)
        .expect(200)
        .then(resp => resp.body);
    t.true(user_resp.username === user.username);
});

ava('authorization: revoke authorization', async t => {
    const user = await createFakeUser(t, {
        password: 'pass',
        status: 'accepted',
    });

    const authorization_resp = await t.context.api
        .post('v1/authorization')
        .auth(user.username, 'pass')
        .expect(200)
        .then(resp => resp.body);

    const access_token = authorization_resp.access_token.token;

    await t.context.api
        .delete(`v1/authorization/${authorization_resp.authorization._id}`)
        .set('Authorization', `Bearer ${access_token}`)
        .expect(200);

    await t.context.api
        .get('v1/user/me')
        .set('Authorization', `Bearer ${access_token}`)
        .expect(401)
        .then(resp => resp.body)
        .then(body => {
            t.true(body.message === 'Access token is invalid due to the withdrawal of the authorization');
        });
});
