const express = require('express');
const path = require('path');
const pug = require('pug');
const WebSocket = require('ws');
const PORT = 8080;
const app = express();

printerSockets = new Object(); // { printerName: socket }
browserSockets = new Set();

// troubleshooting info
console.log('working directory: ' + __dirname);

///////////////////////////////////////////////////
// express code - USER
///////////////////////////////////////////////////

app.use(express.static(path.join(__dirname, '/')));
app.set("views", path.join(__dirname, "views"));
app.set('view engine', 'pug');

// renders main web page
app.get('/', (req, res) => {
  res.render('index');
  console.log('***root directory accessed***');
});

////////////////////////////////////////////////////
// websocket code - PRINTER
////////////////////////////////////////////////////

const wss= new WebSocket.Server({ noServer: true });

wss.on('connection', (ws, req) => {
  console.log("client connected");
  //console.log(ws);
  //console.log(req.headers) // solo use of req arg in this scope

  ws.on('message', message => {
    if (message == 'ping') {
      console.log('heartbeat received'); 
    } else if (test_json(message)) {

      var messageObj = JSON.parse(message)

      console.log('SERVER RECEIVED', messageObj)

      if (messageObj.questioner == 'browser') {
        /* incoming browser client json format
        {
          'questioner': 'browser', 
          'command': <<<cmd>>>,
          'target': <<<target>>> // (target printer name)
        }*/
        
        if (!(ws in browserSockets)) {
          browserSockets.add(ws)
        }
        
        switch(messageObj.command) {
          /* outgoing command to printer format
          {
            'command': <<<command>>>
          }*/
          case 'client_list':
            console.log('SERVER SENDING to browser', build_printer_list())
            ws.send(build_printer_list());
            break;
          case 'stop_print':
            console.log('STOPPING PRINT for', messageObj.target)

            if (printerSockets) {
              printerSockets[messageObj.target].send(JSON.stringify({'command':'stop'}))
            }
            break;
            
        }
      } else if (messageObj.questioner == 'printer') {
        /* incoming printer client json format
        {
          'questioner': 'printer',
          'printer_name': <<<printer_name>>>
          'completion': <<<compl_percent>>>
        }*/
        update_printers(message, ws); // will update printer socket each time

        if (messageObj.completion) {
          browser_broadcast('completion',
                          messageObj.completion,
                          messageObj.printer_name)
        }
      }
      console.log('CONNECTIONS: (P='+
        Object.keys(printerSockets).length+
        ')(B='+browserSockets.size+')')

    } else {
      console.log(message);
    }
  });

  ws.on('close', () => {
    console.log("client disconnected")
    if (browserSockets.has(ws)) {
      browserSockets.delete(ws)
    } else if (Object.values(printerSockets).indexOf(ws) > -1) {
      delete printerSockets[ws] // DOUBLE CHECK THIS IS WORKING RIGHT
    }
  });
});

const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`)
});

server.on('upgrade', (req, socket, head) => {
  wss.handleUpgrade(req, socket, head, sock => {
    wss.emit('connection', sock, req);
  });
});

/////////////////////////////////////////////////////
// MISC JS
/////////////////////////////////////////////////////

// sends message to all browser clients
function browser_broadcast(key, value, printerName) {
  var msg = {
    [key]:value,
    'printer_name':printerName
  }

  browserSockets.forEach(function each(browser) {
    browser.send(JSON.stringify(msg))
  })
}

// returns number of items in an object
function object_counter(object) {
  var length = 0;
    for( var key in object ) {
        if( object.hasOwnProperty(key) ) {
            ++length;
        }
    }
    return length;
}

// this function is a json detector
function test_json(jsonStr) {
  try {
    JSON.parse(jsonStr);
  } catch(e) {
    return false;
  }
  return true;
};

// updates printers objecdt using message from client
function update_printers(jsonStr, socket) {
  var printer_obj = JSON.parse(jsonStr);
  var name = printer_obj.printer_name;

  printerSockets[name] = socket;
};

// this returns a stringified list of all printer clients
function build_printer_list() {
  var json = []

  for (printer in printerSockets) {
    json.push({"printer_name": printer})
  }

  return JSON.stringify(json)
}

// for debugging...derp => probably remove this function
function debug_print() {
  console.log("\n" + clients.length + ' items in object / contains...');

  for (i=0; i<clients.length; i++) {
    console.log(clients[i].printer_name);
  }
  console.log("");
}







