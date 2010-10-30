import liblo
import math
import HSI2RGB
import Queue

def eventhandler(light,event,message):
    if light.event == event:
        if light.mode == 'flash':
            # Initialize a new flash, with the new target intensity
            # set to 1, final intensity set to 0, hue increment set to
            # 360/5 (5 times to go from red to red), and the saturation
            # set to 1, over 25 ticks up and 25 ticks down.
            numlights = message[0]
            targetintensity = message[1]
            flashinit(light, targetintensity, 0.0, 360.0/numlights, 1.0, 20, 20)
        elif light.mode == 'setcolor':
            light.currenthue, light.currentsaturation, light.currentintensity = args

class eventcall:
    def __init__(self, light, event, message):
        self.caller = light
        self.event = event
        self.message = message

def flashtick(light):
    if light.state == 'upintensity':
        light.currentintensity = light.currentintensity + light.intensityincrement
        if math.fabs(light.currentintensity-light.targetintensity) < math.fabs(light.intensityincrement):
            light.currentintensity = light.targetintensity
            light.targetintensity = light.finalintensity
            light.intensityincrement = (light.targetintensity - light.currentintensity)/light.downticks
            light.state = 'downintensity'
    elif light.state == 'downintensity':
        light.currentintensity = light.currentintensity + light.intensityincrement
        if math.fabs(light.currentintensity-light.targetintensity) < math.fabs(light.intensityincrement):
            light.currentintensity = light.targetintensity
            light.brightnenessincrement = 0
            light.state = 'idle'

def flashinit(light, targetintensity, finalintensity, hueincrement, saturation, upticks, downticks):
    # First, shift the color on each init by the hue increment given to the function.
    light.currenthue = light.currenthue + hueincrement
    # Test for moving the hue outside of the circle.
    if light.currenthue >= 360:
        light.currenthue = light.currenthue - 360
    light.targetintensity = targetintensity
    light.finalintensity = finalintensity
    light.saturation = saturation
    light.upticks = upticks
    light.downticks = downticks

    # Set the state to the initial part of a flash.
    if math.fabs(light.currentintensity-light.targetintensity) < 1.0/255.0:
        light.currentintensity = light.targetintensity
        light.targetintensity = light.finalintensity
        light.intensityincrement = (light.targetintensity - light.currentintensity)/light.downticks
        light.state = 'downintensity'
    else:
        light.state = 'upintensity'
        light.intensityincrement = (light.targetintensity - light.currentintensity)/light.upticks

    light.hueincrement = 0
    light.saturationincrement = 0

class LightObject:
    currenthue = 0.0
    currentintensity = 0.0
    currentsaturation = 1.0
    targethue = 0.0
    targetintensity = 0.0
    targetsaturation = 1.0
    finalhue = 0.0
    finalintensity = 0.0
    finalsaturation = 0.0
    upticks = 10.0
    downticks = 10.0
    hueincrement = 0.0
    intensityincrement = 0.0
    saturationincrement = 0.0
    state = 'idle'
    eventqueue = Queue.Queue(128)
    def __init__(self, IP, event, mode):
        self.event = event
        self.address = liblo.Address(IP,"2222")
        self.mode = mode
    def handleevent(self, event, message):
        self.eventqueue.put(eventcall(self,event,message))
    def handletick(self):
        if self.mode == 'flash':
            flashtick(self)
        R, G, B = HSI2RGB.convert(self.currenthue, self.currentsaturation, self.currentintensity)
        liblo.send(self.address,'/light/color/set',('f', R),('f', G),('f', B))
        while self.eventqueue.empty() == False:
            queuedevent = self.eventqueue.get()
            eventhandler(queuedevent.caller, queuedevent.event, queuedevent.message)
            
            
