const mongoose= require('mongoose');

module.exports = {
    connect: async url => {

        const connect = await mongoose.connect(url, {
            useCreateIndex: true,
            useNewUrlParser: true,
            useFindAndModify: false,
        });
        await require('./../model').register();
        return connect;
    }
};
