import liblo
import time

addresses = [liblo.Address("192.168.1.200","2222"),liblo.Address("192.168.1.201","2222"),liblo.Address("192.168.1.202","2222"),liblo.Address("192.168.1.203","2222"),liblo.Address("192.168.1.204","2222"),liblo.Address("192.168.1.205","2222"),liblo.Address("192.168.1.206","2222"),liblo.Address("192.168.1.207","2222")]

r=0
g=0
b=0

for address in addresses:
    liblo.send(address,'22',('f', r),('f', g),('f', b))
