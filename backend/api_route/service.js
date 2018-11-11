'use strict';
const {createRouter} = require('../lib/resources');

const ServiceResource = {
    list: {},
    create: {},
    get: {},
    update: {},
    delete: {}
};

module.exports = () => createRouter('Service', ServiceResource);
