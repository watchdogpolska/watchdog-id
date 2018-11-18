const http = require('http');

const target = http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'application/json'});
    const body = {headers: req.headers, path: req.url};
    res.write(JSON.stringify(body, true, 2));
    res.end();
});
target.listen(9000);
