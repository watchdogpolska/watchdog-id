'use strict';
const ava = require('ava').default;
const {startServer, stopServer, withAdminUser, createFakeUser, createFakeRole} = require('../lib/tests');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

const createAccessRequest = async (t, body) => {
    const user = Object.assign({
        comment: `test-access-request-${Math.random()}`,
        userId: await createFakeUser(t),
        features: {
            passwordReset: false,
            userProvidedUsername: false,
        },
    }, body);
    return t.context.api.post('v1/access_request')
        .send(user)
        .expect(200)
        .then(resp => resp.body);
};

// ava('pobranie listy żądań dostępu danego użytkownika', withRole(async (t, session, service, role) => {
//
//         await t.context.api
//             .get(`v1/access_request/`)
//             .expect(200)
//             .then(resp => {
//                 t.true(Array.isArray(resp.body));
//                 t.true(resp.body.length > 0);
//             })
//     }
// ));
//
// ava.todo('pobranie listy żądań dostępu danego systemu');
ava('utworzenie żadania dostępu', withAdminUser(async t => {
    const user = await createFakeUser(t);
    const role = await createFakeRole(t);
    console.log("Test role", role);
    const body = {
        usersId: [user._id],
        rolesId: [role._id]
    };
    return createAccessRequest(t, body)
        .then(body => {
            t.true(body.usersId.includes(user._id));
            t.true(body.rolesId.includes(role._id));
            t.true(body.opinions.length > 0, 'Each access request requires at least one opinion.');
            t.true(body.events.length > 0, 'Access request requires on create event.');
            t.true(body.events.some(event => event.status === 'created'))
        })
}));
ava.todo('powiadomienie przełożonego');
ava.todo('powiadomienie operatora systemu');
ava.todo('odwołanie żądania dostępu');
ava.todo('reset hasła wybranego konta');
