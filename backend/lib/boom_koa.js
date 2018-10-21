module.exports = (ctx, boom) => {
    ctx.response.status = boom.output.statusCode;
    ctx.response.set(boom.output.headers);
    ctx.response.body = boom.output.payload;
};
