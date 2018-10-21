const ava = require('ava').default;
const {api} = require('../lib/tests');

ava.beforeEach(async t => {
    const port = Math.round(Math.random() * 10000 + 2000);
    t.context.server = await require('../index')({LISTEN_PORT: port});
    t.context.api = api({
        host: "localhost",
        port
    });
    t.context.fakeUser = {
        "username": `string-${port}`,
        "first_name": "string",
        "second_name": "string",
        "password": "string",
        "status": "pending",
        "email": 'user@example.com',
    };
});

ava.afterEach(t => new Promise((resolve, reject) => {
    t.context.server.once('close', resolve);
    t.context.server.once('error', reject);
    t.context.server.close();
}));

const withSession = fn => async t => {
    await t.context.api.post('v1/user').send(t.context.fakeUser);
    const session = await t.context.api.login(
        t.context.fakeUser.username,
        t.context.fakeUser.password
    );
    await fn(t, session);
};

ava('GET /user as authenticated', withSession((t, session) => t.context.api
        .get(`v1/user/${session.user}`)
        .expect(200)
        .then(resp => t.true(resp.body._id === session.user))
));

ava('make user suspended', withSession((t, session) => t.context.api
    .del(`v1/user/${session.user}`)
    .expect(200)
    .then(resp => {
        t.true(resp.body.status === 'suspended')
    })
));
