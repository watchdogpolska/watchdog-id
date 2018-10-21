const model = require('./../model');
const mongoose = require("mongoose");
const Router = require("koa-router");
var kittySchema = new mongoose.Schema({
  name: String
});
var Kitten = mongoose.model('Kitten', kittySchema);

module.exports = () => {

    return new Router()
        .get("/user", async (ctx) => {
            console.log("Hit GET /user");
            ctx.body = await User.find();
        })
        .post("/user", async (ctx) => {
            const User = mongoose.model('User');
            console.log("Hit POST /user", ctx.request.body);
            const u = User(ctx.request.body);
            var silence = new Kitten(ctx.request.body);
            console.log("User", await silence.save());
            const user = await User(ctx.request.body).save();
            ctx.body = user;
        })
        .all('/', (ctx) => ctx.body = ctx.request.body);
};
