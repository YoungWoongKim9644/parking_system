import socket


#uid_set = set([358723174009, 12345])


class Client:


	def __init__(self, HOST='localhost', PORT=9999):
		self.host = HOST
		self.port = PORT
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connection_init(self):

		print("connection try")

		try:
			self.client_socket.connect((self.host, self.port))
			return True
		except ConnectionRefusedError:
			print("connection refused")
			return False

	def write_msg(self, msg):
		self.client_socket.sendall(msg)

	def conn_close(self):
		self.client_socket.close()
	
	def is_registered(self, uid):

		try:
			print("send msg", uid)
			data = ''
			self.client_socket.sendall(str(uid).encode())


			print("error?")
			recv = self.client_socket.recv(1024).decode()
			print("error!")
			data += recv
			if not recv:
				print("break out")

			print("recv data:", data)
			if data == 'o':
				return True
			elif data == 'x':
				return False

		except RuntimeError:
			print("error occured")
			return False



		"""	
		if uid in uid_set:
			return True
		else:
			return False
		"""

