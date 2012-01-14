import liblo

address = liblo.Address("192.168.0.13","2222")

liblo.send(address,'/1/fader1',('f', .5),('f',0))

