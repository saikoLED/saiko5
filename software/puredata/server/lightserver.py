import lightconfiguration
from liblo import *
import sys, time

print "SaikoControl Light Server Starting..."

lights = lightconfiguration.Lights

class MyServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 2223)

    @make_method('/event/onset', 'ff')
    def onset_callback(self, path, message):
        for light in lights:
            newmessage = (len(lights), message[0], message[1])
            light.handleevent('onset', newmessage)

try:
    server = MyServer()
except liblo.ServerError, err:
    print str(err)
    sys.exit()

server.start()

for light in lights:
    light.handleevent('onset', (len(lights), 1.0, 10))

print "SaikoControl Light Server Started!"

while True:
    for light in lights:
        light.handletick()
    time.sleep(0.03)
        
