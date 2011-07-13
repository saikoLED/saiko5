import liblo
import time

address = liblo.Address("10.0.1.54","2222")
liblo.send(address,'/light/color/set',('f', 0.8),('f', 0),('f',0.2))

