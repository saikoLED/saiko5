import lightevents

Light1 = lightevents.LightObject('192.168.1.3','onset','randflash')
Light2 = lightevents.LightObject('192.168.1.4','onset','randflash')
Light3 = lightevents.LightObject('192.168.1.5','onset','randflash')
Light4 = lightevents.LightObject('192.168.1.6','onset','randflash')
Light5 = lightevents.LightObject('192.168.1.7','onset','randflash')
Light6 = lightevents.LightObject('192.168.1.8','onset','randflash')
Light7 = lightevents.LightObject('192.168.1.9','onset','randflash')
Light8 = lightevents.LightObject('192.168.1.10','onset','randflash')
Light9 = lightevents.LightObject('192.168.1.11','onset','randflash')
Light10 = lightevents.LightObject('192.168.1.12','onset','randflash')
Light11 = lightevents.LightObject('192.168.1.13','onset','randflash')
Light12 = lightevents.LightObject('192.168.1.14','onset','randflash')
Light13 = lightevents.LightObject('192.168.1.15','onset','randflash')
Light14 = lightevents.LightObject('192.168.1.16','onset','randflash')
Light15 = lightevents.LightObject('192.168.1.17','onset','randflash')

Lights = [Light1, Light2, Light3, Light4, Light5]

#Lights = [Light1, Light2, Light3, Light4, Light5, Light6, Light7, Light8, Light9, Light10, Light11, Light12, Light13, Light14, Light15]

# This defines the initial offset in colors.
i=0.0
for Light in Lights:
    Light.currenthue = i
    i = i + 360/len(Lights)
