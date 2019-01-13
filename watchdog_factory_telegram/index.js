// 'use strict';
// const {unauthorized} = require('boom');
// const uuidv4 = require('uuid/v4');
// const Telegraf = require('telegraf');
// const jwt = require('jsonwebtoken');
// const promisify = require('util').promisify;
// const sign = promisify(jwt.sign);
// const verify = promisify(jwt.verify);
//
// const TIMEOUT_MS = 5 * 60 * 1000;
//
// const quote = '```';
//
// module.exports = async (settings) => {
//     const registration = {};
//     const users = {};
//     const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN, {username: process.env.TELEGRAM_BOT_USERNAME});
//     await bot.telegram.getMe().then((botInfo) => {
//         bot.options.username = botInfo.username;
//     });
//
//     const handleRegistration = async (token, chat_id = {}) => {
//         let claim = null;
//         try {
//             claim = await verify(token, settings.JWT_SECRET, {
//                 // issuer: settings.JWT_ISSUER,
//             });
//         } catch (err) {
//             console.log(err);
//             const data = {
//                 err: err.toString(),
//                 token,
//             };
//             const msg = `${quote}\n${JSON.stringify(data, null, 4)}\n${quote}`;
//             await bot.telegram.sendMessage(chat_id, msg, {parse_mode: 'markdown'});
//             return;
//         }
//         if (!registration[claim.uuid]) {
//             await bot.telegram.sendMessage(chat_id, `Unknown request UUID: ${claim.uuid}.`);
//             return;
//         }
//         await registration[claim.uuid](chat_id);
//         await bot.telegram.sendMessage(chat_id, 'Successfully registered!.');
//     };
//     const handleAuthentication = async (token, chat_id = {}) => {
//         let claim = null;
//         try {
//             claim = await verify(token, settings.JWT_SECRET, {
//                 // issuer: settings.JWT_ISSUER,
//             });
//         } catch (err) {
//             console.log(err);
//             const data = {
//                 err: err.toString(),
//                 token,
//             };
//             const msg = `${quote}\n${JSON.stringify(data, null, 4)}\n${quote}`;
//             await bot.telegram.sendMessage(chat_id, msg, {parse_mode: 'markdown'});
//             return;
//         }
//         if (!registration[claim.uuid]) {
//             await bot.telegram.sendMessage(chat_id, 'Unknown request UUID. Create new factor and try again!');
//             return;
//         }
//         await registration[claim.uuid](chat_id);
//         await bot.telegram.sendMessage(chat_id, 'Successfully registered!.');
//     };
//     bot.hears('ping', ctx => ctx.reply('pong!'));
//     bot.hears(/start (.+?)$/, async ctx => {
//         console.log(ctx.message);
//         await handleRegistration(ctx.match[1], ctx.message.chat.id);
//     });
//     bot.hears(/confirm (.+?)$/, async ctx => {
//
//     });
//     bot.startPolling();
//
//     return {
//         name: 'Telegram',
//         registrationChallengeHandler: async (user, requestInput) => {
//             const uuid = uuidv4();
//             const claim = await sign({
//                 uuid: uuid,
//                 aud: 'telegram_factor',
//             }, settings.JWT_SECRET);
//
//             registration[uuid] = (telegram_id) => {
//                 delete request[uuid];
//                 return resolve({telegram_id});
//             };
//
//             return {
//                 uuid: uuid,
//                 claim: claim,
//                 link: `https://telegram.me/${bot.options.username}?start=${claim}`,
//             };
//         },
//         registrationVerificationHandler: (user, requestInput, challenge) => {
//             if (users[challenge.uuid]) {
//                 return {chat_id: users[challenge.uuid]};
//             }
//         },
//         authenticationVerificationHandler: async (user, requestInput, config) => new Promise(async (resolve, reject) => {
//             const uuid = uuidv4();
//             const msg = 'A new request to WatchdogID requires authenticate. Do you want to accept them now?';
//             await bot.telegram.sendMessage(config.chat_id, msg, {
//                 reply_markup: {
//                     inline_keyboard: [
//                         {text: `/accept ${uuid}`},
//                         {text: `/deny ${uuid}`},
//                     ],
//                 },
//             });
//
//             const timeout = setTimeout(() => {
//                 delete registration[uuid];
//                 return reject(unauthorized('The time for verification via Telegram has ended.'));
//             }, TIMEOUT_MS);
//
//             registration[uuid] = (telegram_id) => {
//                 delete request[uuid];
//                 clearTimeout(timeout);
//                 return resolve({telegram_id});
//             };
//         }),
//     };
// };
