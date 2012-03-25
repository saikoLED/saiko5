import liblo
from time import sleep
from address import address 

for i in range(100):
  print i/100.0
  liblo.send(address,'/1/fader5',('f', i/100.0))
  sleep(.05)

