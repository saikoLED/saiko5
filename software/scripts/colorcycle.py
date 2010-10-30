import liblo
import time

addresses = [liblo.Address("192.168.1.122","2222"),liblo.Address("192.168.1.4","2222"),liblo.Address("192.168.1.5","2222"),liblo.Address("192.168.1.6","2222"),liblo.Address("192.168.1.7","2222"),liblo.Address("192.168.1.8","2222"),liblo.Address("192.168.1.9","2222"),liblo.Address("192.168.1.10","2222"),liblo.Address("192.168.1.11","2222"),liblo.Address("192.168.1.12","2222"),liblo.Address("192.168.1.13","2222"),liblo.Address("192.168.1.14","2222"),liblo.Address("192.168.1.15","2222"),liblo.Address("192.168.1.16","2222"),liblo.Address("192.168.1.17","2222")]


r=0
g=0
b=0
colormax = 1
step = 1.0/256
delay = 0.01

while r < colormax :
    for address in addresses:
	liblo.send(address,'22',('f', r),('f', g),('f', b))
    r=r+step
    time.sleep(delay)
    
while True:
    while g < colormax :
	for address in addresses:
		liblo.send(address,'22',('f', r),('f', g),('f', b))
        r=r-step
        g=g+step
        time.sleep(delay)
    while b < colormax :
	for address in addresses:
        	liblo.send(address,'22',('f', r),('f', g),('f', b))
        g=g-step
        b=b+step
        time.sleep(delay)
    while r < colormax :
        for address in addresses:
		liblo.send(address,'22',('f', r),('f', g),('f', b))
        b=b-step
        r=r+step
        time.sleep(delay)
