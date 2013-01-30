import liblo
import time

addresses = [liblo.Address("192.168.1.3","2222"),liblo.Address("192.168.1.4","2222"),liblo.Address("192.168.1.5","2222"),liblo.Address("192.168.1.6","2222"),liblo.Address("192.168.1.7","2222"),liblo.Address("192.168.1.8","2222"),liblo.Address("192.168.1.9","2222"),liblo.Address("192.168.1.10","2222"),liblo.Address("192.168.1.11","2222"),liblo.Address("192.168.1.12","2222"),liblo.Address("192.168.1.13","2222"),liblo.Address("192.168.1.14","2222"),liblo.Address("192.168.1.15","2222"),liblo.Address("192.168.1.16","2222"),liblo.Address("192.168.1.17","2222")]

while True:
    for address in addresses:
        liblo.send(address,'22',('f', 0),('f', 0),('f',0))
#    time.sleep(0.001)
