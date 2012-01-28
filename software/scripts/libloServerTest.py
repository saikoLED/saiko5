import liblo
from time import sleep
s=liblo.Server(2222)
def callback(path,msg):
  print path,msg
s.add_method(None,None,callback)
while s.recv():
  sleep(.001)
