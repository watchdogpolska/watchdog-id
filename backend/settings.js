'use strict';
module.exports.DOMAIN = process.env.DOMAIN || 'id.siecobywatelska.pl';
module.exports.DEFAULT_MAIL_FROM = process.env.DEFAULT_MAIL_FROM || `noreply@${module.exports.DOMAIN}`;
module.exports.MONGODB_URL = process.env.MONGODB_URL || 'mongodb://localhost/test';
module.exports.LISTEN_PORT = process.env.LISTEN_PORT || 3000;
module.exports.SMTP_URL = process.env.SMTP_URL;
module.exports.IMAP_URL = process.env.IMAP_URL;
module.exports.SESSION_LIFETIME = 60 * 15; // 15 minutes
module.exports.JWT_SECRET = process.env.JWT_SECRET || 'xxxx';
module.exports.JWT_ISSUER = process.env.JWT_ISSUER || `https://${module.exports.DOMAIN}`;
module.exports.FACTOR_LIST = [
    './factory/sms_sns',
    './factory/u2f',
    './factory/totp',
    './factory/yub',
];
module.exports.YUBICO_CLIENT_ID = process.env.YUBICO_CLIENT_ID;
module.exports.YUBICO_SECRET_KEY = process.env.YUBICO_SECRET_KEY;
