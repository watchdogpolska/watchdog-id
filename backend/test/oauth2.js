'use strict';
const ava = require('ava').default;
const {startServer, stopServer, createFakeClient, asAdminUser} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('authorization: Authorization Code Flow & refresh_token', asAdminUser(async t => {
    const client =  await createFakeClient(t);

    const {_id: client_id, client_secret} = client;
    const redirect_uri = await t.context.api
        .post('v1/oauth2/authorize')
        .send({
            client_id: client_id,
            response_type: 'code',
            redirect_uri: client.redirect_uri[0],
            scope: 'identify',
            state: 'STATE',
        })
        .expect(302)
        .then(resp => resp.headers.location);
    t.true(!!redirect_uri);

    const url = new URL(redirect_uri);
    t.true(!!url.searchParams.get('code'));
    t.true(url.searchParams.get('state') === 'STATE');

    const token_resp = await t.context.api
        .post('v1/oauth2/token')
        .send({
            grant_type: 'code',
            code: url.searchParams.get('code'),
            client_id: client_id,
            client_secret: client_secret,
        })
        .expect(200)
        .then(resp => resp.body);
    t.true(!!token_resp.access_token);
    t.true(!!token_resp.refresh_token);

    const refreshed_resp = await t.context.api
        .post('v1/oauth2/token')
        .send({
            grant_type: 'refresh_token',
            refresh_token: token_resp.refresh_token.token,
            client_id: client_id,
            client_secret: client_secret,
        })
        .expect(200)
        .then(resp => resp.body);

    t.true(!!refreshed_resp.access_token);
    t.true(!!refreshed_resp.refresh_token);
    t.true(refreshed_resp.access_token !== token_resp.access_token);
    t.true(refreshed_resp.refresh_token !== token_resp.refresh_token);
}));

ava('authorization: Implicit Flow', asAdminUser(async t => {
    const client =  await createFakeClient(t);

    const {_id: client_id} = client;
    const redirect_uri = await t.context.api
        .post('v1/oauth2/authorize')
        .send({
            client_id: client_id,
            response_type: 'id_token token',
            redirect_uri: client.redirect_uri[0],
            scope: 'identify',
            state: 'STATE',
        })
        .expect(302)
        .then(resp => resp.headers.location);
    t.true(!!redirect_uri);

    const url = new URL(redirect_uri);
    const params = new URLSearchParams(url.hash.slice(1));
    t.true(!!params.get('access_token'));
    t.true(!!params.get('token_type'));
    t.true(!!params.get('expires_in'));
    t.true(!!params.get('id_token'));
    t.true(params.get('state') === 'STATE');
}));
