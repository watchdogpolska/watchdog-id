'use strict';
const ava = require('ava').default;
const {startServer, stopServer, asAdminUser, createFakeUser, createFakeAccessRequest, avaMockNodeMailer} = require('../lib/tests');

const nodemailerMock = avaMockNodeMailer(ava);

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('access request/opinions: list', asAdminUser(async t => {
    const access_request = await createFakeAccessRequest(t);
    const opinion = access_request.opinions[0];
    const resp = await t.context.api
        .get(`v1/access_request/${access_request._id}/opinion`)
        .expect(200)
        .then(resp => resp.body);
    t.true(Array.isArray(resp));
    t.true(!!resp.find(x => x._id === opinion._id));
}));

ava('access request/opinions: get', asAdminUser(async t => {

    const access_request = await createFakeAccessRequest(t);
    const opinion = access_request.opinions[0];

    const resp = await t.context.api
        .get(`v1/access_request/${access_request._id}/opinion/${opinion._id}`)
        .expect(200)
        .then(resp => resp.body);
    t.true(!Array.isArray(resp));
    t.true(resp._id === opinion._id);
}));

ava('access request/opinions: accept', asAdminUser(async t => {
    const access_request = await createFakeAccessRequest(t);
    const opinion = access_request.opinions[0];
    const resp = await t.context.api
        .post(`v1/access_request/${access_request._id}/opinion/${opinion._id}`)
        .send({
            status: 'accepted'
        })
        .expect(200)
        .then(resp => resp.body);
    t.true(!Array.isArray(resp));
    t.true(resp._id === opinion._id);
    t.true(resp.status === 'accepted');
    const resp_access_request = await t.context.api
        .get(`v1/access_request/${access_request._id}`)
        .expect(200)
        .then(resp => resp.body);

    t.true(!Array.isArray(resp_access_request));

    t.true(resp_access_request._id === access_request._id);
    t.true(resp_access_request.status === 'accepted');
    t.true(resp_access_request.events.some(event => event.status === 'accepted'));
    t.true(resp_access_request.events.some(event => event.status === 'queued'))
}));

ava('access request/opinions: forbidden accept opinions for other user',
    asAdminUser(async t => {
        const access_request = await createFakeAccessRequest(t);
        const opinion = access_request.opinions[0];
        const standard_user = await createFakeUser(t, {
            password: 'pass',
            status: 'accepted'
        });
        await t.context.api.login(standard_user.username, 'pass');
        const user_logged_in = await t.context.api.get('v1/user/me').expect(200).then(resp => resp.body);
        t.true(user_logged_in.username === standard_user.username);
        await t.context.api
            .post(`v1/access_request/${access_request._id}/opinion/${opinion._id}`)
            .send({
                status: 'accepted'
            })
            .expect(403);
    })
);
ava('access request/opinions: reject', asAdminUser(async t => {
    const access_request = await createFakeAccessRequest(t);
    const opinion = access_request.opinions[0];
    const resp = await t.context.api
        .post(`v1/access_request/${access_request._id}/opinion/${opinion._id}`)
        .send({
            status: 'rejected'
        })
        .expect(200)
        .then(resp => resp.body);
    t.true(!Array.isArray(resp));
    t.true(resp._id === opinion._id);
    t.true(resp.status === 'rejected');
    const resp_access_request = await t.context.api
        .get(`v1/access_request/${access_request._id}`)
        .expect(200)
        .then(resp => resp.body);
    t.true(!Array.isArray(resp_access_request));

    t.true(resp_access_request._id === access_request._id);
    t.true(resp_access_request.status === 'rejected');
    t.true(resp_access_request.events.some(event => event.status === 'rejected'));
    t.true(!resp_access_request.opinions.some(opinion => opinion.status !== 'rejected'));
    t.true(!resp_access_request.events.some(event => event.status === 'queued'))
}));
