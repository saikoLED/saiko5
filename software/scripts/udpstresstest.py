import socket
import time

host = "192.168.1.116"
port = 2222

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto("22", (host,port))
    time.sleep(0.00003)
