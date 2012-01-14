import liblo

address = liblo.Address("192.168.0.3","2222")

liblo.send(address,'/light/color/set',('f', 0),('f', 0),('f', 0))

