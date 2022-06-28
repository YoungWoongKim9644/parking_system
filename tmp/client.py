import sys
import socket

class Client:
	
	def __init__(self, HOST='localhost', PORT=9999):
		self.host = HOST
		self.port = PORT
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connection_init(self):
		self.client_socket.connect((self.host, self.port))

	def write_msg(self, msg):
		self.client_socket.sendall(msg)

	def conn_close(self):
		self.client_socket.close()


