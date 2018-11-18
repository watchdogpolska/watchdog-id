'use strict';

const cookieEncode = (obj) => Object.entries(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join("&");

module.exports = {
    cookieEncode
}
