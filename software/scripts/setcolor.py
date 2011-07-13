import liblo

address = liblo.Address("192.168.1.200","2222")

liblo.send(address,'/light/color/set',('f', 1),('f', 0),('f', .3))

