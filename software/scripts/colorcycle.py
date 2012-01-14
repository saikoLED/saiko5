import liblo
import time

addresses = [liblo.Address("18.224.0.163","2222")]


r=0
g=0
b=0
colormax = 1
step = 1.0/256
delay = 0.01

while r < colormax :
    for address in addresses:
	liblo.send(address,'2222',('f', r),('f', g),('f', b))
    r=r+step
    time.sleep(delay)
    
while True:
    while g < colormax :
	for address in addresses:
		liblo.send(address,'2222',('f', r),('f', g),('f', b))
        r=r-step
        g=g+step
        time.sleep(delay)
    while b < colormax :
	for address in addresses:
        	liblo.send(address,'2222',('f', r),('f', g),('f', b))
        g=g-step
        b=b+step
        time.sleep(delay)
    while r < colormax :
        for address in addresses:
		liblo.send(address,'2222',('f', r),('f', g),('f', b))
        b=b-step
        r=r+step
        time.sleep(delay)
