import lightevents

Light1 = lightevents.LightObject('192.168.1.3','onset','flash')
Light2 = lightevents.LightObject('192.168.1.4','onset','flash')
Light3 = lightevents.LightObject('192.168.1.5','onset','flash')
Light4 = lightevents.LightObject('192.168.1.6','onset','flash')
Light5 = lightevents.LightObject('192.168.1.7','onset','flash')
Light6 = lightevents.LightObject('192.168.1.8','onset','flash')
Light7 = lightevents.LightObject('192.168.1.9','onset','flash')
Light8 = lightevents.LightObject('192.168.1.10','onset','flash')
Light9 = lightevents.LightObject('192.168.1.11','onset','flash')
Light10 = lightevents.LightObject('192.168.1.12','onset','flash')
Light11 = lightevents.LightObject('192.168.1.13','onset','flash')
Light12 = lightevents.LightObject('192.168.1.14','onset','flash')
Light13 = lightevents.LightObject('192.168.1.15','onset','flash')
Light14 = lightevents.LightObject('192.168.1.16','onset','flash')
Light15 = lightevents.LightObject('192.168.1.17','onset','flash')

Lights = [Light1, Light2, Light3, Light4, Light5, Light6, Light7, Light8, Light9, Light10, Light11, Light12, Light13, Light14, Light15]

# This defines the initial offset in colors.
i=0.0
for Light in Lights:
    Light.currenthue = i
    i = i + 360/len(Lights)
    
