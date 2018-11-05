'use strict';
module.exports.DOMAIN = process.env.DOMAIN || 'id.siecobywatelska.pl';
module.exports.DEFAULT_MAIL_FROM = process.env.DEFAULT_MAIL_FROM || `noreply@${module.exports.DOMAIN}`;
module.exports.MONGODB_URL = process.env.MONGODB_URL || 'mongodb://localhost/test';
module.exports.LISTEN_PORT = process.env.LISTEN_PORT || 3000;
module.exports.SMTP_URL = process.env.SMTP_URL;
module.exports.IMAP_URL = process.env.IMAP_URL;
module.exports. SESSION_LIFETIME = 60 * 15; // 15 minutes
