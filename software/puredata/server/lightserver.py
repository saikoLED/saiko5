import lightconfiguration
from liblo import *
import sys, time

print "SaikoControl Light Server Starting..."

lights = lightconfiguration.Lights

class MyServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 2223)

#    @make_method(None, None)
#    def fallback(self, path, args):
#        print "received unknown message '%s'" % path

    @make_method('/event/onset', 'f')
    def onset_callback(self, path, message):
        for light in lights:
            light.handleevent('onset', (len(lights), message[0]))

try:
    server = MyServer()
except liblo.ServerError, err:
    print str(err)
    sys.exit()

server.start()

for light in lights:
    light.handleevent('onset', (len(lights), 1.0))

print "SaikoControl Light Server Started!"

while True:
    for light in lights:
        light.handletick()
    time.sleep(0.01)
        
