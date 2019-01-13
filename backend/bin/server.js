'use strict';
const notifications = require('./../lib/notifications');
const pEvent = require("p-event");
const settings = require('./../settings');
const signals = require('./../lib/signals');
const factory = require('./../factory');
const db = require('./../lib/db');
const createServerAndListen = require("./../lib/server");

const main = async (options) => {
    const config = Object.assign({}, settings, process.env, options);

    await db.connect(config.MONGODB_URL);
    notifications.connect(signals);
    await Promise.all(config.FACTOR_LIST.map(require).map(factory.use));
    const server = await createServerAndListen(app, port, host);

    await Promise.race([
        ...["SIGINT", "SIGHUP", "SIGTERM"].map(s =>
            pEvent(process, s, {
                rejectionEvents: ["uncaughtException", "unhandledRejection"],
            }),
        )
    ]);
    console.log("Close server");
    await server.stop();
    console.log("Server closed");
    console.log("Close database");
    await db.disconnect();
    console.log("Database closed")
};

main()
    .then(() => console.log('Process success'))
    .catch(console.error)
    .finally(() => console.log('Proccess end'));
