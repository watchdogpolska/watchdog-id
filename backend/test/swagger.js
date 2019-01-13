'use strict';
const ava = require('ava').default;
const {startServer, stopServer} = require('../lib/tests');
const SwaggerParser = require('swagger-parser');

ava.beforeEach(startServer);
ava.afterEach(stopServer);

ava('/apiDocs rendered', async t=> {
    const resp = await t.context.api.get('apiDocs').expect(200);
    t.true(!!resp.body);
});

['redoc', 'swagger'].forEach(ui => {
    ava(`/${ui} rendered`, async t => {
        const resp = await t.context.api.get(ui).expect(200);
        t.true(!!resp.body);
        t.true(resp.headers['content-type'].includes('text/html'));
    });
});

ava('/swagger/swagger-ui.css rendered', async t => {
    const resp = await t.context.api.get('swagger/swagger-ui.css').expect(200);
    t.true(!!resp.body);
    t.true(resp.headers['content-type'].includes('text/css'));
});

ava('/apiDocs valid swagger file', async t => {
    await SwaggerParser.validate(await t.context.api.get('apiDocs').then(resp => resp.body))
});
