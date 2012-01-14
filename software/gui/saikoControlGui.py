#!/usr/bin/python
#----------------------------------------------------------------------
# Jacked cube color picker to control LightBrick v1.0 AKA Optimus Shine
# Daniel Taub 23 Sept 2010
#----------------------------------------------------------------------
#
# Based on CUBECOLOURDIALOG Widget, Python Code By:
# Andrea Gavana, @ 16 Aug 2007
# 
# 



#todo:
# loop hue control
# light selection
# actual control
# buffer to record random playing, display as gradient, and loop selection
# remember last color or query network for it on startup, remember custom colors

MODES = ['CK','Simu','Saiko']
CURRENT_MODE = 2  # 2= saiko liblo
MODE_NAME = MODES[CURRENT_MODE]

IP_ADDRESSES = ["192.168.0.13"] #, ...

from array import array

import sys,thread
from threading import Thread

class ThreadScript(Thread):
	
#	lock this 
	mqueue = {} 
	
	def __init__(self,lc,buffer,seqPat):
		lam=ThreadScript.getRunScript(lc,buffer,seqPat)

#		tid=thread.start_new_thread(lam,(None,))
		#return "started thread ",tid	
		Thread.__init__(self)
		self.run = lam
		#lam()
	@staticmethod
	def checkExit(d):
		return mqueue.has_key(id)

#	@staticmethod
#	def RunScriptThread(lc,buffer,seqPat):
#		tid=thread.start_new_thread(getRunScript(lc,whichBuf,seqPat))
#		print "started thread ",tid

	@staticmethod
	def getRunScript(lc,buffer,seqPat):
		#yeild somfunction
		def nameless():
			#myBuf=buffer[:]
			r = buffer[0][:]
			g = buffer[1][:]
			b = buffer[2][:]

			bLen=len(r)
			checkAtCount=100
			counter = 0
			lcounter=0
			sendAtCount = 10000 #use time interval?	
			while 1:
				rgb = [r[lcounter%bLen],g[lcounter%bLen],b[lcounter%bLen]] 
				#test if thread needs to exit in static	structure
#				if counter%checkAtCount == 0:
#					if ThreadScript.checkExit():#   if ThreadScript.checkExit(thread.get_ident()):
#						thread.exit()
				if counter%sendAtCount == 0:
					lc.SendLights(*rgb)			
					lcounter+=1
				counter+=1
		return nameless

class LightController:
	def __init__(self,):	
		a127 = range(127)
		b127 = [127-i for i in a127[:]]
		self.recording = False
		self.currentBuffer = (array('B',range(255)),
					array('B',[255-i for i in range(255)]),
					array('B',a127+[128]+b127))
		self.buffers = (self.currentBuffer,)


	def loopBuffer(self,whichBuf=0,seqPat = '/\\'):
		activeBuf = self.buffers[whichBuf]
		t=ThreadScript(self,activeBuf,seqPat)
		t.start()
		print 'started thread: ',t
	def NewBuffer(self,initList=[]):
		self.currentBuffer = array('B',initList)
		self.buffers+=(self.currentBuffer,)
	
	def SendLightsSimu(self,r,g,b):
		print r,g,b

	def SendLightsCK(self,r,g,b):
	    # struct.pack(fmt, magic, ver, type, seq, port, flags, timerVal V, uni, 0, 0, 0, 0, data)
		levels  = [r,g,b]*10
		arr = array.array('B', levels)
		
		out = struct.pack("LHHLBxHLB255s", 0x4adc0104, 0x0001, 0x0101, 0, 0, 0, -1, 0, arr.tostring())
		socket(AF_INET, SOCK_DGRAM).sendto(out, (IP_ADDRESS, port))
        	
	#	print r,g,b
	
	def SendLightsSaiko(self,r,g,b):
        	fRed = r/255.0
		fGreen = g/255.0
 		fBlue = b/255.0
                for address in addresses:
                        liblo.send(address,'/light/color/set',('f',fRed),('f',fGreen),('f',fBlue))

	def UpdateControlSet(self,listOfLights):
		pass


if CURRENT_MODE == 2:
	import liblo
        addresses = [liblo.Address(IP_ADDRESS,"2222") for IP_ADDRESS in IP_ADDRESSES]
	LightController.SendLights = LightController.SendLightsSaiko
elif CURRENT_MODE == 0:
	import struct
	import array
	from socket import socket, AF_INET, SOCK_DGRAM
	port = 6038
	LightController.SendLights = LightController.SendLightsCK
else:
	LightController.SendLights = LightController.SendLightsSimu



import wx
import os
import sys

try:
	dirName = os.path.dirname(os.path.abspath(__file__))
except:
	dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
	from agw import cubecolourdialog as ccdSource
#	from agw.cubecolourdialog import *

except ImportError: # if it's not there locally, try the wxPython lib.
#	from wx.lib.agw.cubecolourdialog import *
	import wx.lib.agw.cubecolourdialog as ccdSource
	#import cubecolourdialog as ccdSource

from wx.lib.agw.cubecolourdialog import Colour
#Colour = ccdSource.Colour

from colourWidgets import RGBCube,HSVWheel,BrightCtrl
from myWidget import PowerCtrl,XYPanel#RGBCube = ccdSource.RGBCube
#HSVWheel = ccdSource.HSVWheel
#BrightCtrl = ccdSource.BrightCtrl
CustomPanel = ccdSource.CustomPanel
ColourPanel = ccdSource.ColourPanel
#colourAttributes  = ccdSource.colourAttributes
#colourMaxValues  = ccdSource.colourMaxValues
colourAttributes = ["r", "g", "b", "h", "s", "v","t","c","p"]
colourMaxValues = [255, 255, 255, 359, 255, 255, 359, 255, 255]
Distance = ccdSource.Distance
Vertex = ccdSource.Vertex
Top = ccdSource.Top
Left = ccdSource.Left
Right = ccdSource.Right

RED=ccdSource.RED
GREEN=ccdSource.GREEN
BLUE=ccdSource.BLUE

LineDescription = ccdSource.LineDescription
Slope = ccdSource.Slope
FindC = ccdSource.FindC	
PointOnLine = ccdSource.PointOnLine
Intersection = ccdSource.Intersection
PtFromAngle = ccdSource.PtFromAngle

RECT_WIDTH = ccdSource.RECT_WIDTH

def newColInit(self,colour):
		wx.Colour.__init__(self)
		self.r = colour.Red()
		self.g = colour.Green()
		self.b = colour.Blue()
		self._alpha = 1
		self.ToHSV()

#	Can't call this function in versio 2.6 of wxpython because
#		of bug, so redefine init manually:
Colour.__init__ = newColInit

class NewColour(Colour):
	constrainPower = False
	def __init__(self,colour):

                super(NewColour,self).__init__(colour)
		self.ToXYZ()
		
	def ToHSL(self):
		self.H = self.h
		self.L = (510.0-(self.s)) * (self.v/255.0)
		self.S = self.s * self.v
		if self.L <= 255.0:
			lfactor = self.L
		else:
			lfactor = 510.0 - self.L
	
		self.S /= lfactor 
		self.L /= 2.0
		
	def ToXYZ(self):
	
		self.c = self.s #2*(max(self.b,max(self.r,self.g)) - min(self.b,min(self.r,self.g)))
		self.p = min(255,self.r+self.g+self.b) 
		self.t = self.h
		
		if self.constrainPower:
				# do stuff for ToHSV and ToRGB 
				pass
		else:
				pass
				
	def ToHSV(self):
		Colour.ToHSV(self)
		self.ToXYZ()

	def ToRGB(self):
		Colour.ToRGB(self)
		self.ToXYZ()

	def HSL_ToRGB_HSV(self):

		self.h = self.H
		ell = self.L/255.0 * 2
		ess = self.S/255.0
		
		if ell <= 1:
			ess *= ell
		else:
			ess *= (2 - ell)

		self.v = int(255.0*((ell + ess) / 2))
		self.s = int(255.0*(2*ess /(ell+ess)))
		Colour.ToRGB(self)
		
		
	def XYZ_ToRGB_HSV(self):
		maxVal = self.p
		delta = maxVal * self.c / 255.0
		minVal = maxVal - delta
		
		hue = float(self.t)
		
		if self.t > 300 or self.t <=60:
			#red max
			r=int(maxVal)
			
			if self.t > 300:
				g = int(minVal)
				hue = (hue - 360.0)/60.0
				b = int(-(hue*delta - minVal))
			else:
				b=int(minVal)
				hue = hue/60.0
				g = int(hue*delta+minVal)
		elif self.t > 60 and self.t < 180:
			#green max
			g = int(maxVal)
			hue = (hue/60.0 - 2.0)*delta
			
			if self.t < 120:
				b = int(minVal)
				r = int(minVal - hue)
			else:
				r = int(minVal)
				b = int(minVal + hue)
		else:
			b = int(maxVal)
			hue = (hue/60.0 - 4.0)*delta
            
			if self.t < 240:
					r = int(minVal)
					g = int(minVal - hue)
			else:
					g = int(minVal)
					r = int(minVal + hue)
		
		power = self.p
		sumpower = r+g+b / 1.0
		if sumpower:
			self.r=int(r*power/sumpower)
			self.g=int(g*power/sumpower)
			self.b=int(b*power/sumpower)
							# 
							# self.h = self.t
							# self.s = self.c
							# power = self.p 
							# self.v = self.p
							# Colour.ToRGB(self)
							# colorpower =  (self.r + self.g + self.b) / 1
							# if colorpower:
							# 	self.r=int(self.r*power/colorpower)
							# 	self.g=int(self.g*power/colorpower)
							# 	self.b=int(self.b*power/colorpower)
							# 
		Colour.ToHSV(self)
        
class NewCustomPanel(CustomPanel):

	def __init__(self,parent,cd):
#		super(NewCustomPanel,self).__init__(parent,cd)
		CustomPanel.__init__(self,parent,cd)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
	def OnLeftDown(self, event):
		"""
		Handles the ``wx.EVT_LEFT_DOWN`` for L{CustomPanel}.

		:param `event`: a `wx.MouseEvent` event to be processed.
		"""

		x, y = event.GetX(), event.GetY()

		selX = (x - self._customColourRect.x)/(self._smallRectangleSize.x + self._gridSpacing)
		selY = (y - self._customColourRect.y)/(self._smallRectangleSize.y + self._gridSpacing)
		ptr = selX + selY*8

#		dc = wx.ClientDC(self)
#		self.PaintHighlight(dc, False)
		self._colourSelection = ptr

		self._mainDialog._colour = NewColour(self._customColours[self._colourSelection])

#		self.PaintCustomColour(dc, selX, selY)
#		self.PaintHighlight(dc, True)
		self._mainDialog.DrawAll()

		self._mainDialog.SendLightsIfManual()

class CubeColourFrame(wx.Frame):
	"""
	This is the CubeColourFrame main class implementation.
	"""

	manualSend = False
	def __init__(self, parent, title, lc = None, colourData=None, agwStyle=ccdSource.CCD_SHOW_ALPHA):
		"""
		Default class constructor.

		:param `colourData`: a standard `wx.ColourData` (as used in `wx.ColourFrame`;
		:param `agwStyle`: can be either ``None`` or ``ccdSource.CCD_SHOW_ALPHA``, depending if you want
		 to hide the alpha channel control or not.
		"""

		if lc == None:
			self.lc = LightController()
		else:
			self.lc = lc
#		wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_("Optimus Shine"),
#						   pos=wx.DefaultPosition, size=(900, 900), style=wx.DEFAULT_DIALOG_STYLE)

		wx.Frame.__init__(self, parent, -1, title, pos=wx.DefaultPosition, size=(900, 900)) 
		if colourData:
			self._colourData = colourData
		else:
			self._colourData = wx.ColourData()
			self._colourData.SetColour(wx.Colour(128, 128, 128))

#		self._oldColour = Colour(self._colourData.GetColour())
		
		self._colour = NewColour(self._colourData.GetColour())

		self._inMouse = False
		self._initOver = False
		self._inDrawAll = False
		self._agwStyle = agwStyle

		self.mainPanel = wx.Panel(self, -1)


		self.xyzSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "XYZ")

		self.hsvSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB")
		self.rgbValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB Values")
		self.hsvValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB Values")

		self.xyzValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "XYZ Values")

		self.rgbSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB")
		self.curcolSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Current Color")
#		self.alphaSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")
#		self.alphaValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")

		self.rgbBitmap = RGBCube(self.mainPanel)
		self.hsvBitmap = HSVWheel(self.mainPanel)
		self.brightCtrl = BrightCtrl(self.mainPanel)
#		self.alphaCtrl = AlphaCtrl(self.mainPanel)
		self.powerCtrl = PowerCtrl(self.mainPanel)
		self.xyPanel = XYPanel(self.mainPanel)


#		self.showAlpha = wx.CheckBox(self.mainPanel, -1, "Show Alpha Control")
		self.autoSend = wx.CheckBox(self.mainPanel, -1, "AutoSend on\nColorChange")
		self.customColours = NewCustomPanel(self.mainPanel, self._colourData)

		self.addCustom = wx.Button(self.mainPanel, -1, "Add to custom colours")
		
#		self.okButton = wx.Button(self.mainPanel, -1, "Ok")
		self.cancelButton = wx.Button(self.mainPanel, -1, "Cancel")
		self.sendButton = wx.Button(self.mainPanel, -1, "Send")

#		self.oldColourPanel = ColourPanel(self.mainPanel, style=wx.SIMPLE_BORDER)
		self.newColourPanel = ColourPanel(self.mainPanel, style=wx.SIMPLE_BORDER)
		
		self.redSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
								   style=wx.SP_ARROW_KEYS)
		self.greenSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
									 style=wx.SP_ARROW_KEYS)
		self.blueSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
									style=wx.SP_ARROW_KEYS)
		self.hueSpin = wx.SpinCtrl(self.mainPanel, -1, "0", min=-1, max=360,
								   style=wx.SP_ARROW_KEYS)
		self.saturationSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
										  style=wx.SP_ARROW_KEYS)
		self.brightnessSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
										  style=wx.SP_ARROW_KEYS)
		self.tintSpin = wx.SpinCtrl(self.mainPanel, -1, "0", min=-1, max=360,
								   style=wx.SP_ARROW_KEYS)
		self.chromaSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
										  style=wx.SP_ARROW_KEYS)
		self.powerSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
										  style=wx.SP_ARROW_KEYS)
#		self.alphaSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
#									 style=wx.SP_ARROW_KEYS)
#		self.accessCode = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
#		self.htmlCode = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
#	   self.webSafe = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
#	   self.htmlName = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
		
		self.SetProperties()
		self.DoLayout()

		self.spinCtrls = [self.redSpin, self.greenSpin, self.blueSpin,
						  self.hueSpin, self.saturationSpin, self.brightnessSpin,
							self.tintSpin, self.chromaSpin, self.powerSpin]

		for spin in self.spinCtrls:
			spin.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)

#		self.Bind(wx.EVT_SPINCTRL, self.OnAlphaSpin, self.alphaSpin)
		
#		self.Bind(wx.EVT_BUTTON, self.OnOk, self.okButton)
#		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelButton)
		self.Bind(wx.EVT_BUTTON, self.OnSend, self.sendButton)
		self.Bind(wx.EVT_BUTTON, self.OnAddCustom, self.addCustom)


		self.Bind(wx.EVT_CHECKBOX, self.OnAutoSend)
#		self.Bind(wx.EVT_CHECKBOX, self.OnShowAlpha)
#		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUp)

		self.Centre(wx.BOTH)

		wx.CallAfter(self.InitDialog)
		
		
	def SetProperties(self):
		""" Sets some initial properties for L{CubeColourDialog} (sizes, values). """

#		self.okButton.SetDefault()
#		self.oldColourPanel.SetMinSize((-1, 50))
		self.newColourPanel.SetMinSize((-1, 50))
		self.redSpin.SetMinSize((60, -1))
		self.greenSpin.SetMinSize((60, -1))
		self.blueSpin.SetMinSize((60, -1))
		self.hueSpin.SetMinSize((60, -1))
		self.saturationSpin.SetMinSize((60, -1))
		self.brightnessSpin.SetMinSize((60, -1))
		self.tintSpin.SetMinSize((60, -1))
		self.chromaSpin.SetMinSize((60, -1))
		self.powerSpin.SetMinSize((60, -1))
#		self.alphaSpin.SetMinSize((60, -1))
#		self.showAlpha.SetValue(1)
		self.autoSend.SetValue(1)
#		self.accessCode.SetInitialSize((80, -1))
#		self.webSafe.SetInitialSize((80, -1))
#		self.htmlCode.SetInitialSize((80, -1))


	def DoLayout(self):
		""" Layouts all the controls in the L{CubeColourDialog}. """

		windowSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer = wx.GridBagSizer(10, 5)
		hsvValueSizer = wx.StaticBoxSizer(self.hsvValueSizer_staticbox, wx.VERTICAL)
		hsvGridSizer = wx.GridSizer(2, 3, 2, 10)
		rgbValueSizer = wx.StaticBoxSizer(self.rgbValueSizer_staticbox, wx.HORIZONTAL)
		rgbGridSizer = wx.GridSizer(2, 3, 2, 10)
		xyzValueSizer = wx.StaticBoxSizer(self.xyzValueSizer_staticbox, wx.HORIZONTAL)
		xyzGridSizer = wx.GridSizer(2, 3, 2, 10)
#		alphaValueSizer = wx.StaticBoxSizer(self.alphaValueSizer_staticbox, wx.VERTICAL)
#		alphaGridSizer = wx.BoxSizer(wx.VERTICAL)
		customSizer = wx.BoxSizer(wx.VERTICAL)
		buttonSizer = wx.BoxSizer(wx.VERTICAL)
		sendbuttonSizer = wx.BoxSizer(wx.VERTICAL)

		sendSizer = wx.BoxSizer(wx.HORIZONTAL)
		curcolSizer = wx.StaticBoxSizer(self.curcolSizer_staticbox, wx.VERTICAL)

		panelSizer = wx.BoxSizer(wx.VERTICAL)
#		htmlSizer1 = wx.BoxSizer(wx.HORIZONTAL)
#		htmlSizer2 = wx.BoxSizer(wx.VERTICAL)
#		htmlSizer_a = wx.BoxSizer(wx.VERTICAL)
#		htmlSizer_b = wx.BoxSizer(wx.VERTICAL)
		xyzSizer = wx.StaticBoxSizer(self.xyzSizer_staticbox, wx.HORIZONTAL)
		
		hsvSizer = wx.StaticBoxSizer(self.hsvSizer_staticbox, wx.HORIZONTAL)
		rgbSizer = wx.StaticBoxSizer(self.rgbSizer_staticbox, wx.VERTICAL)
#		autosendSizer = wx.StaticBoxSizer(self.autosendSizer_staticbox, wx.VERTICAL)

#		mainSizer.Add(self.showAlpha, (0, 0), (1, 1), wx.LEFT|wx.TOP, 10)
#		htmlLabel1 = wx.StaticText(self.mainPanel, -1, "HTML Code")
#		htmlLabel2 = wx.StaticText(self.mainPanel, -1, "Web Safe")
#		htmlSizer_a.Add(htmlLabel1, 0, wx.TOP, 3)
#		htmlSizer_b.Add(htmlLabel2, 0, wx.TOP, 3)
#		htmlSizer_a.Add(self.htmlCode, 0, wx.TOP, 3)
#		htmlSizer_b.Add(self.webSafe, 0, wx.TOP, 3)
#
#		htmlSizer1.Add(htmlSizer_a, 0)
#		htmlSizer1.Add(htmlSizer_b, 0, wx.LEFT, 10)
#		mainSizer.Add(htmlSizer1, (1, 0), (1, 1), wx.LEFT|wx.RIGHT, 10)
		
#		htmlLabel3 = wx.StaticText(self.mainPanel, -1, "HTML Name")
#		htmlSizer2.Add(htmlLabel3, 0, wx.TOP|wx.BOTTOM, 3)
#		htmlSizer2.Add(self.htmlName, 0)
		
#		mainSizer.Add(htmlSizer2, (1, 1), (1, 1), wx.LEFT|wx.RIGHT, 10)

		customLabel = wx.StaticText(self.mainPanel, -1, "Custom Colours")
		customSizer.Add(customLabel, 0, wx.BOTTOM, 3)
		customSizer.Add(self.customColours, 0)
		customSizer.Add(self.addCustom, 0, wx.TOP|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
		mainSizer.Add(customSizer, (1, 1), (1, 1),wx.LEFT|wx.RIGHT, 5)
#		panelSizer.Add(accessSizer, 0, wx.TOP, 5)


		xyzSizer.Add(self.xyPanel, 0, wx.ALL, 15)
		xyzSizer.Add(self.powerCtrl, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 15)
		mainSizer.Add(xyzSizer, (2, 2), (1, 1), wx.ALL|wx.EXPAND, 10)
		
		rgbSizer.Add(self.rgbBitmap, 0, wx.ALL, 15)
		mainSizer.Add(rgbSizer, (2, 0), (1, 1), wx.ALL|wx.EXPAND, 10)
		hsvSizer.Add(self.hsvBitmap, 0, wx.ALL, 15)
		hsvSizer.Add(self.brightCtrl, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 15)
		mainSizer.Add(hsvSizer, (2, 1), (1, 1), wx.ALL|wx.EXPAND, 10)
#		alphaSizer.Add(self.alphaCtrl, 0, wx.TOP|wx.ALIGN_CENTER, 15)
#		mainSizer.Add(alphaSizer, (2, 2), (1, 1), wx.ALL|wx.EXPAND, 10)
		
#		oldLabel = wx.StaticText(self.mainPanel, -1, "Old Colour")
#		panelSizer.Add(oldLabel, 0, wx.BOTTOM, 3)
#		panelSizer.Add(self.oldColourPanel, 0, wx.BOTTOM|wx.EXPAND, 20)
#		newLabel = wx.StaticText(self.mainPanel, -1, "New Colour")
#		accessLabel = wx.StaticText(self.mainPanel, -1, "MS Access Code")
#		accessSizer.Add(accessLabel, 0, wx.BOTTOM, 3)
#		accessSizer.Add(self.accessCode, 0)

		sendbuttonSizer.Add(self.sendButton, 0,wx.TOP,10)
		
		curcolSizer.Add(self.newColourPanel, 0, wx.EXPAND)
		sendSizer.Add(self.autoSend)	
		sendSizer.Add(sendbuttonSizer,0,wx.LEFT,20)
		curcolSizer.Add(sendSizer)
#		panelSizer.Add(newLabel, 0, wx.TOP, 3)
#		panelSizer.Add(autosendSizer, 0, wx.TOP)
#	panelSizer.Add((0, 0), 1, wx.EXPAND)
#	panelSizer.Add((1,0), 1, wx.BOTTOM)

#		panelSizer.Add(sendbuttonSizer, 0, wx.TOP, 5)
#		panelSizer.Add(autosendSizer, 0, wx.BOTTOM, 10)

		mainSizer.Add(curcolSizer, (1, 0), (1, 1), wx.ALL|wx.EXPAND, 10)


		redLabel = wx.StaticText(self.mainPanel, -1, "Red")
		rgbGridSizer.Add(redLabel, 0)
		greenLabel = wx.StaticText(self.mainPanel, -1, "Green")
		rgbGridSizer.Add(greenLabel, 0)
		blueLabel = wx.StaticText(self.mainPanel, -1, "Blue")
		rgbGridSizer.Add(blueLabel, 0)
		rgbGridSizer.Add(self.redSpin, 0, wx.EXPAND)
		rgbGridSizer.Add(self.greenSpin, 0, wx.EXPAND)
		rgbGridSizer.Add(self.blueSpin, 0, wx.EXPAND)
		rgbValueSizer.Add(rgbGridSizer, 1, 0, 0)
		mainSizer.Add(rgbValueSizer, (3, 0), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)


		hueLabel = wx.StaticText(self.mainPanel, -1, "Hue")
		hsvGridSizer.Add(hueLabel, 0)
		saturationLabel = wx.StaticText(self.mainPanel, -1, "Saturation")
		hsvGridSizer.Add(saturationLabel, 0)
		brightnessLabel = wx.StaticText(self.mainPanel, -1, "Brightness")
		hsvGridSizer.Add(brightnessLabel, 0)
		hsvGridSizer.Add(self.hueSpin, 0, wx.EXPAND)
		hsvGridSizer.Add(self.saturationSpin, 0, wx.EXPAND)
		hsvGridSizer.Add(self.brightnessSpin, 0, wx.EXPAND)
		hsvValueSizer.Add(hsvGridSizer, 1, wx.EXPAND)
		mainSizer.Add(hsvValueSizer, (3, 1), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)

		xyzValueSizer.Add(xyzGridSizer, 1, 0, 0)
		mainSizer.Add(xyzValueSizer, (3, 2), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)

		tintLabel = wx.StaticText(self.mainPanel, -1, "Tint")
		xyzGridSizer.Add(tintLabel, 0)
		chromaLabel = wx.StaticText(self.mainPanel, -1, "Chroma")
		xyzGridSizer.Add(chromaLabel, 0)
		powerLabel = wx.StaticText(self.mainPanel, -1, "Power")
		xyzGridSizer.Add(powerLabel, 0)
		xyzGridSizer.Add(self.tintSpin, 0, wx.EXPAND)
		xyzGridSizer.Add(self.chromaSpin, 0, wx.EXPAND)
		xyzGridSizer.Add(self.powerSpin, 0, wx.EXPAND)
#		alphaLabel = wx.StaticText(self.mainPanel, -1, "Alpha")
#		alphaGridSizer.Add(alphaLabel, 0)
#		alphaGridSizer.Add(self.alphaSpin, 0, wx.EXPAND|wx.TOP, 10)
#		alphaValueSizer.Add(alphaGridSizer, 1, wx.EXPAND)
#		mainSizer.Add(alphaValueSizer, (3, 2), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
#		buttonSizer.Add(self.okButton, 0, wx.BOTTOM, 3)

		buttonSizer.Add(self.cancelButton, 0)
		mainSizer.Add(buttonSizer, (3, 3), (1, 1), wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
		mainSizer.Hide(buttonSizer)

		self.mainPanel.SetAutoLayout(True)
		self.mainPanel.SetSizer(mainSizer)
		mainSizer.Fit(self.mainPanel)
		mainSizer.SetSizeHints(self.mainPanel)

#		if self.GetAGWWindowStyleFlag() & ccdSource.CCD_SHOW_ALPHA == 0:
#			mainSizer.Hide(self.showAlpha)
#			mainSizer.Hide(alphaSizer)
#			mainSizer.Hide(alphaValueSizer)
		
		windowSizer.Add(self.mainPanel, 1, wx.EXPAND)
		self.SetAutoLayout(True)
		self.SetSizer(windowSizer)
		windowSizer.Fit(self)
		windowSizer.SetSizeHints(self)
		self.Layout()

		self.mainSizer = mainSizer
		self.windowSizer = windowSizer
#		self.alphaSizers = [alphaSizer, alphaValueSizer]
		

	def InitDialog(self):
		""" Initialize the L{CubeColourDialog}. """

		hsvRect = self.hsvBitmap.GetClientRect()
		self._centre = wx.Point(hsvRect.x + hsvRect.width/2, hsvRect.y + hsvRect.height/2)

		xyRect = self.xyPanel.GetClientRect()
		self._centre2 = wx.Point(xyRect.x + xyRect.width/2, xyRect.y + xyRect.height/2)

		self._redLen = Distance(Vertex, Top)
		self._greenLen = Distance(Vertex, Left)
		self._blueLen = Distance(Vertex, Right)

		self.CalcSlopes()
		self.CalcCuboid()
		self.CalcRects()
		self.CalcRects2()

		self.SetSpinVals()

		self._initOver = True
		wx.CallAfter(self.Refresh)
						

	def CalcSlopes(self):
		""" Calculates the line slopes in the RGB colour cube. """

		self._lines = {RED: LineDescription(), GREEN: LineDescription(), BLUE: LineDescription}
		
		self._lines[RED].slope = Slope(Top, Vertex)
		self._lines[GREEN].slope = Slope(Left, Vertex)
		self._lines[BLUE].slope = Slope(Right, Vertex)

		for i in xrange(3):
			self._lines[i].x = Vertex.x
			self._lines[i].y = Vertex.y
			self._lines[i].c = FindC(self._lines[i])


	def CalcCuboid(self):
		""" Calculates the RGB colour cube vertices. """

		rLen = (self._colour.r*self._redLen)/255.0
		gLen = (self._colour.g*self._greenLen)/255.0
		bLen = (self._colour.b*self._blueLen)/255.0

		lines = [LineDescription() for i in xrange(12)]
		self._cuboid = [None]*8

		self._cuboid[0] = Vertex
		self._cuboid[1] = PointOnLine(Vertex, Top, int(rLen), self._redLen)
		self._cuboid[3] = PointOnLine(Vertex, Left, int(gLen), self._greenLen)
		self._cuboid[7] = PointOnLine(Vertex, Right, int(bLen), self._blueLen)

		lines[0] = self._lines[RED]
		lines[1] = self._lines[GREEN]
		lines[2] = self._lines[BLUE]

		lines[3].slope = self._lines[GREEN].slope
		lines[3].x = self._cuboid[1].x
		lines[3].y = self._cuboid[1].y
		lines[3].c = FindC(lines[3])

		lines[4].slope = self._lines[RED].slope
		lines[4].x = self._cuboid[3].x
		lines[4].y = self._cuboid[3].y
		lines[4].c = FindC(lines[4])

		lines[5].slope = self._lines[BLUE].slope
		lines[5].x = self._cuboid[3].x
		lines[5].y = self._cuboid[3].y
		lines[5].c = FindC(lines[5])

		lines[6].slope = self._lines[GREEN].slope
		lines[6].x = self._cuboid[7].x
		lines[6].y = self._cuboid[7].y
		lines[6].c = FindC(lines[6])

		lines[10].slope = self._lines[BLUE].slope
		lines[10].x = self._cuboid[1].x
		lines[10].y = self._cuboid[1].y
		lines[10].c = FindC(lines[10])

		lines[11].slope = self._lines[RED].slope
		lines[11].x = self._cuboid[7].x
		lines[11].y = self._cuboid[7].y
		lines[11].c = FindC(lines[11])

		self._cuboid[2] = Intersection(lines[3], lines[4])
		self._cuboid[4] = Intersection(lines[5], lines[6])
		self._cuboid[6] = Intersection(lines[10], lines[11])

		lines[7].slope = self._lines[RED].slope
		lines[7].x = self._cuboid[4].x
		lines[7].y = self._cuboid[4].y
		lines[7].c = FindC(lines[7])

		lines[8].slope = self._lines[BLUE].slope
		lines[8].x = self._cuboid[2].x
		lines[8].y = self._cuboid[2].y
		lines[8].c = FindC(lines[8])

		self._cuboid[5] = Intersection(lines[7], lines[8])
				

	def CalcRects(self):
		""" Calculates the brightness control user-selected rect. """

		pt = PtFromAngle(self._colour.h, self._colour.s, self._centre)
		self._currentRect = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
									2*RECT_WIDTH, 2*RECT_WIDTH)


	def CalcRects2(self):
		""" Calculates the brightness control user-selected rect. """

		pt = PtFromAngle(self._colour.t, self._colour.c, self._centre2)
		self._currentRect2 = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
									2*RECT_WIDTH, 2*RECT_WIDTH)



	def DrawMarkers(self, dc=None):
		"""
		Draws the markers for all the controls.

		:param `dc`: an instance of `wx.DC`. If `dc` is ``None``, a `wx.ClientDC` is
		 created on the fly.
		"""

		if dc is None:
			dc = wx.ClientDC(self)

		self.hsvBitmap.DrawMarkers()
		self.rgbBitmap.DrawMarkers()
		self.xyPanel.DrawMarkers()
		self.brightCtrl.DrawMarkers()
		self.powerCtrl.DrawMarkers()
		

	def DrawRGB(self):
		""" Refreshes the RGB colour cube. """

		self.rgbBitmap.Refresh()


	def DrawHSB(self):
		""" Refreshes the HSB colour wheel. """
		self.hsvBitmap.Refresh()

	def DrawXYZ(self):
		""" Refreshes the XYZ colour wheel. """
		self.xyPanel.Refresh()
		

	def DrawBright(self):
		""" Refreshes the brightness control. """

		self.brightCtrl.Refresh()

	def DrawPower(self):
		""" Refreshes the powerness control. """

		self.powerCtrl.Refresh()


	def DrawAlpha(self):
		""" Refreshes the alpha channel control. """
		pass
#		self.alphaCtrl.Refresh()		
	
	def SendLights(self):
		self.lc.SendLights(*self.GetRGBAColour()[:-1])

	def SendLightsIfManual(self):
		if self.manualSend:
			self.lc.SendLights(*self.GetRGBAColour()[:-1])
		
	def SetSpinVals(self):
		""" Sets the values for all the spin controls. """

		self.redSpin.SetValue(self._colour.r)
		self.greenSpin.SetValue(self._colour.g)
		self.blueSpin.SetValue(self._colour.b)
		
		self.hueSpin.SetValue(self._colour.h)
		self.saturationSpin.SetValue(self._colour.s)
		self.brightnessSpin.SetValue(self._colour.v)

		self.powerSpin.SetValue(self._colour.p)
		self.chromaSpin.SetValue(self._colour.c)
		self.tintSpin.SetValue(self._colour.t)
#		self.alphaSpin.SetValue(self._colour._alpha)		
		
		self.SetPanelColours()
		if self.manualSend:
			pass
		else:
			self.SendLights()
#		self.SetCodes()

		

	def SetPanelColours(self):
		""" Assigns colours to the colour panels. """

#		self.oldColourPanel.RefreshColour(self._oldColour)
		self.newColourPanel.RefreshColour(self._colour)
		

#	def SetCodes(self):
#		""" Sets the HTML/MS Access codes (if any) in the text controls. """

#		colour = rgb2html(self._colour)
#		self.htmlCode.SetValue(colour)
#		self.htmlCode.Refresh()

#		if colour in HTMLCodes:
#			colourName, access, webSafe = HTMLCodes[colour]
#			self.webSafe.SetValue(webSafe)
#			self.accessCode.SetValue(access)
#			self.htmlName.SetValue(colourName)
#		else:
#			self.webSafe.SetValue("")
#			self.accessCode.SetValue("")
#			self.htmlName.SetValue("")
		
		
	def OnCloseWindow(self, event):
		"""
		Handles the ``wx.EVT_CLOSE`` event for L{CubeColourDialog}.
		
		:param `event`: a `wx.CloseEvent` event to be processed.
		"""

	   # self.EndModal(wx.ID_CANCEL)


	def OnKeyUp(self, event):
		"""
		Handles the ``wx.EVT_CHAR_HOOK`` event for L{CubeColourDialog}.
		
		:param `event`: a `wx.KeyEvent` event to be processed.
		"""

#		if event.GetKeyCode() == wx.WXK_ESCAPE:
#			self.EndModal(wx.ID_CANCEL)
#
		event.Skip()
		

#	def ShowModal(self):
#		"""
#		Shows L{CubeColourDialog} as a modal dialog. Program flow does
#		not return until the dialog has been dismissed with `EndModal`.
#
#		:note: Overridden from `wx.Dialog`. 
#		"""
#
#		return wx.Dialog.ShowModal(self)


	def SetAGWWindowStyleFlag(self, agwStyle):
		"""
		Sets the L{CubeColourDialog} window style flags.

		:param `agwStyle`: can only be ``ccdSource.CCD_SHOW_ALPHA``.
		"""

#		show = self.GetAGWWindowStyleFlag() & ccdSource.CCD_SHOW_ALPHA
		self._agwStyle = agwStyle
		
#		self.mainSizer.Show(self.alphaSizers[0], show)
#		self.mainSizer.Show(self.alphaSizers[1], show)

		self.mainSizer.Fit(self.mainPanel)
		self.mainSizer.SetSizeHints(self.mainPanel)
		self.mainSizer.Layout()			
		self.windowSizer.Fit(self)
		self.windowSizer.SetSizeHints(self)
		self.Layout()

		self.Refresh()
		self.Update()
		

	def GetAGWWindowStyleFlag(self):
		"""
		Returns the L{CubeColourDialog} window style flags.
		"""

		return self._agwStyle		
		
			
	def OnOk(self, event):
		"""
		Handles the Ok ``wx.EVT_BUTTON`` event for L{CubeColourDialog}.

		:param `event`: a `wx.CommandEvent` event to be processed.
		"""

#		self.EndModal(wx.ID_OK)


	def OnSend(self, event):
		"""
		Handles the Send ``wx.EVT_BUTTON`` event for L{CubeColourDialog}.

		:param `event`: a `wx.CommandEvent` event to be processed.
		"""
		self.SendLights()
		#elf.OnCloseWindow(event)


	def OnCancel(self, event):
		"""
		Handles the Cancel ``wx.EVT_BUTTON`` event for L{CubeColourDialog}.

		:param `event`: a `wx.CommandEvent` event to be processed.
		"""

		self.OnCloseWindow(event)


	def OnAddCustom(self, event):
		"""
		Handles the Add Custom ``wx.EVT_BUTTON`` event for L{CubeColourDialog}.

		:param `event`: a `wx.CommandEvent` event to be processed.
		"""


		self.customColours.AddCustom(self._colour)

	def OnAutoSend(self, event):
		"""
		Enables/disables automatic sending from controls in L{CubeColourDialog}.

		:param `event`: a `wx.CommandEvent` event to be processed.
		"""

 #		agwStyle = self.GetAGWWindowStyleFlag()
		automode = event.IsChecked()

		if automode:
			self.manualSend = False
#			agwStyle |= ccdSource.CCD_SHOW_ALPHA
		else:
			self.manualSend = True
#			agwStyle &= ~ccdSource.CCD_SHOW_ALPHA

#		self.SetAGWWindowStyleFlag(agwStyle)
		

#	def OnShowAlpha(self, event):
#		"""
#		Shows/hides the alpha channel control in L{CubeColourDialog}.
#
#		:param `event`: a `wx.CommandEvent` event to be processed.
 #	   """

 #	   agwStyle = self.GetAGWWindowStyleFlag()
 #	   show = event.IsChecked()

#		if show:
#			agwStyle |= ccdSource.CCD_SHOW_ALPHA
#		else:
#			agwStyle &= ~ccdSource.CCD_SHOW_ALPHA

#		self.SetAGWWindowStyleFlag(agwStyle)
		

	def OnSpinCtrl(self, event):
		"""
		Handles the ``wx.EVT_SPINCTRL`` event for RGB and HSB colours.

#	def OnShowAlpha(self, event):
#		"""
#		Shows/hides the alpha channel control in L{CubeColourDialog}.
#
#		:param `event`: a `wx.CommandEvent` event to be processed.
 #	   """

 #	   agwStyle = self.GetAGWWindowStyleFlag()
 #	   show = event.IsChecked()

#		if show:
#			agwStyle |= ccdSource.CCD_SHOW_ALPHA
#		else:
#			agwStyle &= ~ccdSource.CCD_SHOW_ALPHA

#		self.SetAGWWindowStyleFlag(agwStyle)
	def MyAssignColourValue(self, attribute, colourVal, maxVal, position):
		if attribute == 'h' or attribute == 't':
			if colourVal>maxVal:
				colourVal = colourVal-maxVal-1
			elif colourVal < 0:
				colourVal = maxVal+1-colourVal
		self.AssignColourValue(attribute, colourVal, maxVal, position)		

	def OnSpinCtrl(self, event):
		"""
		Handles the ``wx.EVT_SPINCTRL`` event for RGB and HSB colours.

		:param `event`: a `wx.SpinEvent` event to be processed.
		"""

		obj = event.GetEventObject()
		position = self.spinCtrls.index(obj)
		colourVal = event.GetInt()

		attribute, maxVal = colourAttributes[position], colourMaxValues[position]
		
		self.MyAssignColourValue(attribute, colourVal, maxVal, position)
#		if self.manualSend:
#			pass
#		else:
#			self.SendLights()

#	def OnAlphaSpin(self, event):
#		"""
#		Handles the ``wx.EVT_SPINCTRL`` event for the alpha channel.
#
#		:param `event`: a `wx.SpinEvent` event to be processed.
#		"""
#
#		colourVal = event.GetInt()
#		originalVal = self._colour._alpha
#		if colourVal != originalVal and self._initOver:
#			if colourVal < 0:
#				colourVal = 0
#			if colourVal > 255:
#				colourVal = 255
#
#			self._colour._alpha = colourVal
#			self.DrawAlpha()
			

	def AssignColourValue(self, attribute, colourVal, maxVal, position):
		""" Common code to handle spin control changes. """

		originalVal = getattr(self._colour, attribute)
		if colourVal != originalVal and self._initOver:
			
			if colourVal < 0:
				colourVal = 0
			if colourVal > maxVal:
				colourVal = maxVal

			setattr(self._colour, attribute, colourVal)
			if position < 3:
				self._colour.ToHSV()
#				self._colour.ToXYZ()
			elif position < 6:
				self._colour.ToRGB()				
#				self._colour.ToXYZ()
			else:
				self._colour.XYZ_ToRGB_HSV()

			self.DrawAll()
			

	def DrawAll(self):
		""" Draws all the custom controls after a colour change. """

		if self._initOver and not self._inDrawAll:
			self._inDrawAll = True
			dc1=dc2=dc3=None
			#dc1 = wx.ClientDC(self.hsvBitmap)
			self.hsvBitmap.DrawMarkers(dc1)
			
			#dc2 = wx.ClientDC(self.rgbBitmap)
			self.rgbBitmap.DrawMarkers(dc2)
			#self.rgbBitmap.DrawLines(dc2)

			#dc3 = wx.ClientDC(self.brightCtrl)
			self.brightCtrl.DrawMarkers(dc3)

#			dc4 = wx.ClientDC(self.alphaCtrl)
			self.xyPanel.DrawMarkers(dc1)
#			self.alphaCtrl.DrawMarkers(dc4)
			
			self.CalcCuboid()
			self.CalcRects()
			self.CalcRects2()

			self.DrawRGB()
			self.DrawHSB()
			self.DrawXYZ()
			self.DrawBright()
			self.DrawPower()
#			self.DrawAlpha()
			
			self.SetSpinVals()
			self._inDrawAll = False


	def GetColourData(self):
		""" Returns a wxPython compatible `wx.ColourData`. """

		self._colourData.SetColour(self._colour.GetPyColour())
		return self._colourData


	def GetRGBAColour(self):
		""" Returns a 4-elements tuple of red, green, blue, alpha components. """

		return (self._colour.r, self._colour.g, self._colour.b, self._colour._alpha)

	
	def GetHSVAColour(self):
		""" Returns a 4-elements tuple of hue, saturation, brightness, alpha components. """

		return (self._colour.h, self._colour.s, self._colour.v, self._colour._alpha)


class MyApp(wx.App):
	def OnInit(self):
		frame = CubeColourFrame(None,title="Optimus Shine")#None, "Simple wxPython App")
		self.SetTopWindow(frame)
		import time
		print "Print statements go to this stdout window by default."
		frame.Show(True)
		return True

if __name__ == '__main__': 
	app = MyApp(redirect=True)
	app.MainLoop()

