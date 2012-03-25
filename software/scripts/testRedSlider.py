import liblo
from time import sleep

from address import address 
for i in range(50):
   print i/50.
   liblo.send(address,'/1/fader1',('f', i/50.))
   sleep(.1)
