# This code is modified from the developer of the module
# https://github.com/websocket-client/websocket-client

import json
import logging
import ssl
import time
import websocket

_logger = logging.getLogger('octoprint.plugins.printfarmer')

class SocketServer(object):
	
	def __init__(self, url, port, on_server_message):
		_logger.info("url: ", url)
		
		def on_message(ws, message):
			on_server_message(ws, message)
			_logger.info("SERVER RECEIVED: ", message)

		def on_error(ws, error):
			_logger.info(error)

		def on_close(ws):
			_logger.info("server closed")
			
		hostUrl = "ws://{}:{}".format(url, port)

		self.ws = websocket.WebSocketApp(url = hostUrl,
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	
	def connected(self):
		_logger.info("connected to server")
		return self.ws.sock and self.ws.sock.connected
		
	def close(self):
		_logger.info("closing connection to server")
		self.ws.keep_running = False
		self.ws.close()

	def run(self):
		_logger.info("running printer plugin")
		#self.ws.run_forever()
		self.ws.run_forever(sslopt = {"cert_reqs": ssl.CERT_NONE})
		
	# suboptimal - try/catch not working! - try to find a better way...use json.loads()?
	def test_json(self, data): 
		if len(data) >  0:
			if json.dumps(data)[0] == "{" and json.dumps(data)[-1] == "}":
				return True
			return False

	def send_data(self, data, ping = False):
		_logger.info("attempting to send data")
		if ping:
			self.ws.send(data)
		else:
			if self.test_json(data):
				self.ws.send(json.dumps(data)) 
			else:
				self.ws.send(data)