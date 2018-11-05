'use strict';
const ava = require('ava').default;
const {startServer, stopServer, asAdminUser, createFakeUser, createFakeRole, createFakeAccessRequest, avaMockNodeMailer} = require('../lib/tests');

const nodemailerMock = avaMockNodeMailer(ava);

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('access request: list by user access', asAdminUser(async (t) => {
    const access_request_visible = await createFakeAccessRequest(t);
    const access_request_filtered = await createFakeAccessRequest(t);
    const query = {
        accessUserId: access_request_visible.usersId,
    };

    const resp = await t.context.api
        .get('v1/access_request/')
        .query(query)
        .expect(200);

    t.true(Array.isArray(resp.body));
    t.true(resp.body.some(access_request => access_request._id === access_request_visible._id));
    t.true(!resp.body.some(access_request => access_request._id === access_request_filtered._id));
}));

ava('access request: list by role', asAdminUser(async (t) => {
    const access_request_visible = await createFakeAccessRequest(t);
    const access_request_filtered = await createFakeAccessRequest(t);

    const resp = await t.context.api
        .get('v1/access_request/')
        .query({
            roleId: access_request_visible.rolesId[0],
        })
        .expect(200);

    t.true(Array.isArray(resp.body));
    t.true(resp.body.some(access_request => access_request._id === access_request_visible._id));
    t.true(!resp.body.some(access_request => access_request._id === access_request_filtered._id));
}));

const createFakeUserWithManager = async (t) => {
    const managerUser = await createFakeUser(t);
    const employeUser = await createFakeUser(t, {
        manager: managerUser._id,
    });

    t.true(employeUser.manager === managerUser._id);
    return {managerUser, employeUser};
};

ava('access request: list by opinioner', asAdminUser(async (t) => {
    const {employeUser} = await createFakeUserWithManager(t);

    const access_request_visible = await createFakeAccessRequest(t, {
        usersId: [employeUser._id],
    });
    const access_request_filtered = await createFakeAccessRequest(t);

    const resp = await t.context.api
        .get('v1/access_request/')
        .query({
            opinionUserId: access_request_visible.opinions[0].userId,
        })
        .expect(200);

    t.true(Array.isArray(resp.body));
    t.true(resp.body.some(access_request => access_request._id === access_request_visible._id));
    t.true(!resp.body.some(access_request => access_request._id === access_request_filtered._id));
}));

ava('access request: create', asAdminUser(async t => {
    const user = await createFakeUser(t);
    const role = await createFakeRole(t);
    const body = {
        usersId: [user._id],
        rolesId: [role._id],
    };
    const resp = await createFakeAccessRequest(t, body);

    t.true(resp.usersId.includes(user._id));
    t.true(resp.rolesId.includes(role._id));
    t.true(resp.opinions.length > 0, 'Each access request requires at least one opinion.');
    t.true(resp.events.length > 0, 'Access request requires on create event.');
    t.true(resp.events.some(event => event.status === 'created'));
}));
ava('access request: notify manager of on access request create', asAdminUser(async t => {
    const {managerUser, employeUser} = await createFakeUserWithManager(t);
    await createFakeAccessRequest(t, {
        usersId: [employeUser._id],
    });

    const sentMail = nodemailerMock.mock.sentMail();

    const mail = sentMail.find(x => x.to === managerUser.email);
    t.true(!!mail);
    t.true(mail.headers['X-Event-Type'] === 'accessRequestCreated');
    t.true(sentMail.filter(x => x.to === managerUser.email).length === 1);
}));
ava('powiadomienie operatora systemu', asAdminUser(async t => {
    const {managerUser, employeUser} = await createFakeUserWithManager(t);
    await createFakeAccessRequest(t, {
        usersId: [employeUser._id],
    });
    const sentMail = nodemailerMock.mock.sentMail();

    const mail = sentMail.find(x => x.to === managerUser.email);
    t.true(!!mail);
    t.true(mail.headers['X-Event-Type'] === 'accessRequestCreated');
    t.true(sentMail.filter(x => x.to === managerUser.email).length === 1);
}));

ava.todo('odwołanie żądania dostępu');
ava.todo('reset hasła wybranego konta');
