'use strict';

const signals = {'*': []};

module.exports = {
    connect: (name, fn) => {
        if(!signals[name]){
            signals[name] = new Set([fn]);
        }
        signals[name] = new Set([fn, ...signals[name]])
    },
    disconnect: (name, fn) => signals[name].remove(fn),
    send: async (name, args) => {
        if (!name in signals) {
            return;
        }
        const to_send = [...signals['*'], ...signals[name]];
        await Promise.all(to_send
            .map(fn => {
                fn(...args)
            })
        )
    }
};
