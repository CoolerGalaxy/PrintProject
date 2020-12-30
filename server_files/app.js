const express = require('express');
const path = require('path');
const pug = require('pug');
const WebSocket = require('ws');
const PORT = 8080;
const app = express();

clients = [];
clients.push({"printer_name": 'frank'}) // for testing //
clients.push({"printer_name": 'henry'}) // for testing //

// troubleshooting info
console.log('working directory: ' + __dirname);

///////////////////////////////////////////////////
// express code - USER
///////////////////////////////////////////////////

app.use(express.static(path.join(__dirname, 'js')));
app.set("views", path.join(__dirname, "views"));
app.set('view engine', 'pug');

// renders main web page
app.get('/', (req, res) => {
  res.render('index', {
    "clients": clients
  });

  console.log('***root directory accessed***');
});

// for shuttling commands back to client
app.post('/cmd', (req, res) => {

  console.log('button press detected')

});

////////////////////////////////////////////////////
// websocket code - PRINTER
////////////////////////////////////////////////////

const wss= new WebSocket.Server({ noServer: true });

wss.on('connection', ws => {

  console.log("client connected");
  ws.send("client received message\n");

  ws.on('message', message => {
    if (message == 'ping') {

      ws.send('heartbeat detected by server\n');
      console.log('ping received'); 
    } else if (test_json(message)) {
      console.log("i see JSON");
      /*{
        "printer_name": printer_name
      }*/

      update_obj(message);
      debug_print();

      // need frontend communication to client //

      //console output - verify printer communication
      var printer_obj = JSON.parse(message);
      console.log('message received from ' + printer_obj.printer_name);
      ws.send(printer_obj.printer_name + ", the server says hi!");
    } else {
      //console output - generic communication
      console.log(message);
      ws.send('generic message received');
    }
  });

  ws.on('close', () => {
    console.log("client disconnected")
  });
});

const server = app.listen(PORT);

server.on('upgrade', (req, socket, head) => {
  wss.handleUpgrade(req, socket, head, sock => {
    wss.emit('connection', sock, req);
  });
});

/////////////////////////////////////////////////////
// MISC JS
/////////////////////////////////////////////////////

// this function is a json detector
function test_json(jsonStr) {
  try {
    JSON.parse(jsonStr);
  } catch(e) {
    return false;
  }
  return true;
};

// updates client list using message from client
function update_obj(jsonStr) {
  var detected = false; // yuck, find a better way
  var printer_obj = JSON.parse(jsonStr);

  for (i=0; i<clients.length; i++) {
    if (clients[i].printer_name == printer_obj.printer_name) {
      clients[i] = printer_obj;
      detected = true;
    }
  }
  if (detected == false) {
    clients.push(printer_obj);
    console.log('added: ' + clients[clients.length-1].printer_name);
  }
};

// for debugging...derp
function debug_print() {
  console.log("\n" + clients.length + ' items in object / contains...');

  for (i=0; i<clients.length; i++) {
    console.log(clients[i].printer_name);
  }
  console.log("");
}