'use strict';
module.exports.MONGODB_URL = process.env.MONGODB_URL || 'mongodb://localhost/test';
module.exports.LISTEN_PORT = process.env.LISTEN_PORT || 3000;
module.exports.SMTP_URL = process.env.SMTP_URL;
module.exports.MAIL_FROM = 'Adam Dobrawy <watchdog_id@jawnosc.tk>';
module.exports.IMAP_URL = process.env.IMAP_URL;

module.exports. SESSION_LIFETIME = 60 * 15; // 15 minutes
