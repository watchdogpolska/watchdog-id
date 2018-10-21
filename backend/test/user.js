const ava = require('ava').default;
const request = require('superagent');

const api = host => ({
    post: (path, body = {}) => request.post(`http://${host}/${path}`, body),
    get: (path) => request.get(`http://${host}/${path}`)
});

ava.beforeEach(async t => {
    const port = Math.round(Math.random() * 10000 + 2000);
    t.context.server = await require('../index')({LISTEN_PORT: port});
    t.context.api = api(`localhost:${port}`);
});

ava.afterEach(t => new Promise((resolve, reject) => {
    t.context.server.once('close', resolve);
    t.context.server.once('error', reject);
    t.context.server.close();
}));

ava('foo', async t => {
    await new Promise(resolve => setTimeout(resolve, 3000));
    const resp = await t.context.api.post('v1/user', {
        "username": "string",
        "first_name": "string",
        "second_name": "string",
        "password": "string",
        "status": "pending"
    });
    t.true(resp.body.username === 'string');

});
