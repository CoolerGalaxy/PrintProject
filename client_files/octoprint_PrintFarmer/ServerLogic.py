import logging
from threading import Thread
from time import sleep
from .SocketServer import SocketServer

url = "ws://192.168.1.96:8080" # hard coded temp code for testing
_logger = logging.getLogger('octoprint.plugins.printfarmer')

class ServerLogic(object):
	
	def __init__(self, plugin):
		self.socket = None
		self.server_url = plugin.server_url
		self.server_port = plugin.server_port
		self.printer_name = plugin.printer_name
			
	def update_prep(self):
		return {
			"printer_name": self.printer_name
		}

	def send_printer_update(self):
		''' format...
		{
			"printer_name": printer_name
		}
		'''
		try:
			# hard coded temp code for testing
			self.socket.send_data(data = {"printer_name": "frank"})
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
			
	def loop(self):
		try:
			self.socket = SocketServer(url = url)
			wst = Thread(target=self.socket.run)
			wst.start()
			sleep(1) # figure out async operations with websocket module!!!
			
			self.socket.send_data(data='server received')
			self.send_printer_update()
			
			''' because infinite loop?? '''
			''' triggering octoprint safe mode / find a better way to maintain connection!!!
			while(True):
				if self.socket.connected():
					self.send_heartbeat()
				sleep(10)
			'''
		except Exception as e:
			_logger.info("error starting main loop")
			_logger.info(e)

