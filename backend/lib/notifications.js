'use strict';
const mongoose = require('mongoose');

const accessRequestCreated = async (ctx, access_request) => {
    const User = mongoose.model('User');

    const mail = require('./mail');
    const users = await User.find({_id: access_request.opinions.map(opinion => opinion.userId)});
    for (const user of users) {
        await mail.accessRequestCreated(user, access_request);
    }
};

const userCreated = async () => {

};

const serviceCreated = async () => {

};

const roleCreated = async () => {

};

const accessRequestAccepted = async () => {

};

const connect = signals => {
    signals.connect('userCreated', userCreated);
    signals.connect('serviceCreated', serviceCreated);
    signals.connect('roleCreated', roleCreated);
    signals.connect('accessRequestCreated', accessRequestCreated);
    signals.connect('accessRequestAccepted', accessRequestAccepted);
};

module.exports = {
    connect,
};
