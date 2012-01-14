import liblo

from address import address

liblo.send(address,'/light/color/set',('f', 0),('f', 0),('f', 0))

