'use strict';

const signals = {
    '*': new Set(),
};

module.exports = {
    connect: (name, fn) => {
        if (!signals[name]) {
            signals[name] = new Set([fn]);
        }
        signals[name] = new Set([fn, ...signals[name]]);
    },
    disconnect: (name, fn) => signals[name].remove(fn),
    send: async function (name) {
        if (!name in signals || !signals[name]) {
            if (process.env.NODE_ENV !== 'production') {
                console.error(`Nobody to consume signal '${name}'.`);
            }
            return;
        }
        const to_send = [...signals['*'], ...signals[name]];
        await Promise.all(to_send
            .map(fn =>
                fn(...Array.prototype.slice.call(arguments, 1))
            )
        );
    },
};
