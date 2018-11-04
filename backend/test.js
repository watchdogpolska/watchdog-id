const Ajv = require('ajv');

var ajv = new Ajv({removeAdditional: 'all'});
var schema = {
    additionalProperties: false,
    properties: {
        first_name: {type: 'string'},
        second_name: {type: 'string'},
        username: {type: 'string'},
    },
    required: ['first_name', 'second_name', 'username']
};

var data = {
    _id: '5bd926406b34913acda327b4',
    first_name: 'Adam',
    second_name: 'Dobrawy',
    username: 'adobrawy',
    email: 'aa@jawnosc.tk',
    password_hash:
        'c2NyeXB0AA4AAAAIAAAAAWCHIErN87IUKYtHRBNbziPVOxxdjDyCkRwlraNTWrl/ES/yTBPzyI7WdhwMyXFLgBpDTf4jmPqwxoHHF3QsWanN7HF8pnSYQCqggVI4hKEr',
    __v: 0
};

var validate = ajv.compile(schema);

console.log(validate(data)); // true
console.log(data); // { "foo": 0, "bar": { "baz": "abc", "additional2": 2 }
