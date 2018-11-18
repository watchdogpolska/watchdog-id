const crypto = require('crypto');
const fs = require('fs');
const {pem2jwk} = require('pem-jwk');

// Usage:
// node keygen rsa_public.key rsa_private.key

const {publicKey, privateKey} = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: {type: 'pkcs1', format: 'pem'},
    privateKeyEncoding: {type: 'pkcs1', format: 'pem'}
});

if (process.argv.length <= 3) {
    console.log(publicKey);
    console.log(privateKey);
}else{
    console.log(process.argv[2]);
    fs.writeFileSync(process.argv[2], publicKey);
    fs.writeFileSync(process.argv[3], privateKey);
}

console.log(pem2jwk(publicKey));
