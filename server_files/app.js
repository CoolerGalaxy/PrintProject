var express = require('express');
var app = express();
const PORT = 8080;

// troubleshooting info
console.log('working directory: ' + __dirname);

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/' + 'index.html');
    console.log('***root directory accessed***');
});

app.get('/pi', (req, res) => {
    console.log('***pi directory accessed***');
    console.log('received request: ' , req.query);

    if (req.query.Heartbeat == 'true') {
        console.log('*****Heartbeat Detected*****');
        res.send("You're alive!");
    };
});

app.listen(PORT, function() {
    console.log('Listening on port ' + PORT);
});