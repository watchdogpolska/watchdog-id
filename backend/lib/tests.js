const request = require('supertest');
const api = (options) => {
    const path = `http://${options.host}:${options.port}/`;
    const agent = request.agent(path);
    agent.login = (username, password) => agent
        .post(`v1/user/${username}/session`)
        .send({password})
        .expect(200)
        .then(resp => resp.body);
    return agent;
};

module.exports = {
    api
}
