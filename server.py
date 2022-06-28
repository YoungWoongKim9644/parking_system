import socket

HOST = 'localhost'
PORT = 9999


uid_set = set([358723174009, 12345])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = (HOST,PORT)
print('Starting up on {} port {}'.format(*server_addr))
sock.bind(server_addr)

sock.listen()
sock.settimeout(10)
while True:

    try:
        print('waiting for a connection')
        connection, client_addr = sock.accept()
        try:
            print('connection from', client_addr)

            while True:

                data = int(connection.recv(1024).decode())
                print('received {!r}'.format(data))

                if data in uid_set:
                    send = 'o'
                else:
                    send = 'x'

                connection.sendall(send.encode())
                print("send msg : ", send)
        except RuntimeError:

            print("closing current connection")
            connection.close()

    except socket.timeout:
        print("timeout occured")
        connection.close()