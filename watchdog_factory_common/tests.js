'use strict';
const mockUser = {_id: '123'};

const genericFactorTest = factorTest => async t => {
    const factor = await factorTest.getFactor();
    const factory_instance = {
        _id: '123',
        name: 'my-name',
        challenge: {},
        config: {},
    };

    if (factorTest.registration.challenge) {
        const challenge_reg_input = await factorTest.registration.challenge();
        await factor.registrationChallengeHandler(mockUser, factory_instance, challenge_reg_input);
    }

    const verification_reg_input = await factorTest.registration.verification(factor, factory_instance);
    await factor.registrationVerificationHandler(mockUser, factory_instance, verification_reg_input);

    let challenge;
    if(factorTest.authentication.challenge){
        const auth_req_input = await factorTest.authentication.challenge();
        challenge = await factor.authenticationChallengeHandler(mockUser, factory_instance, auth_req_input);
    }
    const auth_ver_input = await factorTest.authentication.verification(factor, challenge, factory_instance);
    const result = await factor.authenticationVerificationHandler(mockUser, factory_instance, auth_ver_input);
    t.true(result);
};

module.exports = {
    genericFactorTest,
    mockUser,
};
