import socket

TCP_IP = '192.168.1.200'
TCP_PORT = 2222
BUFFER_SIZE = 100
MESSAGE = chr(0x04) + '2222'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print(data)
