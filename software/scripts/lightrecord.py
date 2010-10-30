import sys
import os
import opencv
from opencv import highgui
import liblo
import time
from PIL import Image

address = liblo.Address("192.168.1.200","2222")
camera = highgui.cvCreateCameraCapture(0)
box = (310,230,330,250)

for b in range(0,255):
    for g in range(0,255-b):
        r=255-b-g
        liblo.send(address,'22',('f', float(r)/255.0),('f', float(g)/255.0),('f', float(b)/255.0))
        # To flush the camera buffer =P
        frame = highgui.cvQueryFrame(camera)
        frame = highgui.cvQueryFrame(camera)
        frame = highgui.cvQueryFrame(camera)
        frame = highgui.cvQueryFrame(camera)
        frame = highgui.cvQueryFrame(camera)
        path = "lightrecordresults/test-"+str(r)+"-"+str(g)+"-"+str(b)+".jpg"
        highgui.cvSaveImage(path, frame)
        image = Image.open(path)
	im = image.crop(box)
        pixels = list(im.getdata())
	rsum = 0
	gsum = 0
	bsum = 0
	colorlen = 0
	for p in pixels:
		rsum = rsum + p[0]
		gsum = gsum + p[1]
		bsum = bsum + p[2]
		colorlen = colorlen + 1
	ravg = rsum/colorlen
	gavg = gsum/colorlen
	bavg = bsum/colorlen
	power = ravg+gavg+bavg
	scale = 255.0/power
	print "("+str(r)+" "+str(g)+" "+str(b)+")"+" -> "+"("+str(int(ravg*scale))+" "+str(int(gavg*scale))+" "+str(int(bavg*scale))+")"

