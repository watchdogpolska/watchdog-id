'use strict';
const mongoose = require('mongoose');

module.exports = {
    userSchema: require('./user').schema,
    roleSchema: require('./role'),
    accessRequestSchema: require('./access_request'),
    serviceSchema: require('./service'),
    sessionSchema: require('./session'),
    opinionSchema: require('./opinion'),
    clientSchema: require('./client'),
    authorizationSchema: require('./authorization'),
    factorSchema: require('./factor'),
};

module.exports.register = async () => {
    await mongoose.model('Factor', module.exports.factorSchema);
    await mongoose.model('User', module.exports.userSchema);
    await mongoose.model('Role', module.exports.roleSchema);
    await mongoose.model('AccessRequest', module.exports.accessRequestSchema);
    await mongoose.model('Service', module.exports.serviceSchema);
    await mongoose.model('Session', module.exports.sessionSchema);
    await mongoose.model('Opinion', module.exports.opinionSchema);
    await mongoose.model('Client', module.exports.clientSchema);
    await mongoose.model('Authorization', module.exports.authorizationSchema);
};
