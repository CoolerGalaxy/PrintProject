import json
import logging
from threading import Thread
import time
from .SocketServer import SocketServer

url = "ws://192.168.1.96:8080" # hard coded temp code for testing
_logger = logging.getLogger('octoprint.plugins.printfarmer')

class ServerLogic(object):
	
	def __init__(self, plugin):
		self.socket = None
		self.plugin = plugin
		self.server_url = plugin.server_url
		self.server_port = plugin.server_port
		self.printer_name = plugin.printer_name
			
	def update_prep(self):
		return {
			"questioner": "printer",
			"printer_name": self.printer_name
		}

	def send_printer_update(self):
		''' output format...
		{
			"questioner": "printer",
			"printer_name": printer_name
		}
		'''
		try:
			self.socket.send_data(data = self.update_prep())
			_logger.info("data sent")
		except Exception as e:
			_logger.info("error sending data")
			_logger.info(e)
		pass
		
	def send_heartbeat(self):
		try:
			self.socket.send_data(data = "ping", ping = True)
			_logger.info("heartbeat sent")
		except Exception as e:
			_logger.info("error sending heartbeat")
			_logger.info(e)
			
	def on_server_message(self, ws, message):
		''' input format...
		{
			"command": command
		}
		'''
		try:
			msg = json.loads(message)
			_logger.info(msg)
			
			if msg["command"] == "stop":
				self.plugin._printer.cancel_print()
			
		except Exception as e:
			_logger.info(message)
			_logger.info(e)
			
	def connect_socket(self):
		self.socket = SocketServer(url = self.server_url,
									port = self.server_port,
									on_server_message = self.on_server_message)
		wst = Thread(target = self.socket.run)
		wst.start()
		time.sleep(1) # figure out async operations with websocket module!!!
		
		#self.socket.send_data(data='printer sent generic message')
		self.send_printer_update()
			
	def loop(self):
		last_hb_time = time.time()
		
		while True: # need antoher method / inf. loop triggering octoprint safe mode
			try:
				self.connect_socket()
				while self.socket.connected():
					if time.time() - last_hb_time > 100:
						self.send_heartbeat()
						last_hb_time = time.time()
					time.sleep(1)
			except Exception as e:
				_logger.info(e)
			time.sleep(1)

