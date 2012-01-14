import liblo
import time

address = liblo.Address("192.168.0.3","2222")
liblo.send(address,'/set/rgb',('f', 0.8),('f', 0),('f',0.2))

