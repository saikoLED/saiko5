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

import liblo
address = liblo.Address("192.168.1.200","2222")

class LightController:
	def SendLights(self,r,g,b):
		print r,g,b
		fRed = r/255.0
		fGreen = g/255.0
		fBlue = b/255.0
		liblo.send(address,'/light/color/set',('f',fRed),('f',fGreen),('f',fBlue))
	def UpdateControlSet(self,listOfLights):
		pass

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
	import wx.lib.agw.cubecolourdialog as ccdSource
#	from wx.lib.agw.cubecolourdialog import *

Colour = ccdSource.Colour
RGBCube = ccdSource.RGBCube
HSVWheel = ccdSource.HSVWheel
BrightCtrl = ccdSource.BrightCtrl
CustomPanel = ccdSource.CustomPanel
ColourPanel = ccdSource.ColourPanel
colourAttributes  = ccdSource.colourAttributes
colourMaxValues  = ccdSource.colourMaxValues
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

class NewCustomPanel(CustomPanel):
	def __init__(self,parent,cd):
		super(NewCustomPanel,self).__init__(parent,cd)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
	def OnLeftDown(self,event):
		super(NewCustomPanel,self).OnLeftDown(event)
		self.personalLeftDown()

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

		self._colour = Colour(self._colourData.GetColour())
#		self._oldColour = Colour(self._colourData.GetColour())
		
		self._inMouse = False
		self._initOver = False
		self._inDrawAll = False
		self._agwStyle = agwStyle

		self.mainPanel = wx.Panel(self, -1)

		self.hsvSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB")
		self.rgbValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB Values")
		self.hsvValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB Values")
		self.rgbSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB")
		self.curcolSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Current Color")
#		self.alphaSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")
#		self.alphaValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")

		self.rgbBitmap = RGBCube(self.mainPanel)
		self.hsvBitmap = HSVWheel(self.mainPanel)
		self.brightCtrl = BrightCtrl(self.mainPanel)
#		self.alphaCtrl = AlphaCtrl(self.mainPanel)

#		self.showAlpha = wx.CheckBox(self.mainPanel, -1, "Show Alpha Control")
		self.autoSend = wx.CheckBox(self.mainPanel, -1, "AutoSend on\nColorChange")
		self.customColours = NewCustomPanel(self.mainPanel, self._colourData)
		self.customColours.personalLeftDown = self.SendLightsIfManual

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
		self.hueSpin = wx.SpinCtrl(self.mainPanel, -1, "0", min=0, max=359,
								   style=wx.SP_ARROW_KEYS)
		self.saturationSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
										  style=wx.SP_ARROW_KEYS)
		self.brightnessSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
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
						  self.hueSpin, self.saturationSpin, self.brightnessSpin]

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

		self._redLen = Distance(Vertex, Top)
		self._greenLen = Distance(Vertex, Left)
		self._blueLen = Distance(Vertex, Right)

		self.CalcSlopes()
		self.CalcCuboid()
		self.CalcRects()

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
		self.brightCtrl.DrawMarkers()
		

	def DrawRGB(self):
		""" Refreshes the RGB colour cube. """

		self.rgbBitmap.Refresh()


	def DrawHSB(self):
		""" Refreshes the HSB colour wheel. """

		self.hsvBitmap.Refresh()
		

	def DrawBright(self):
		""" Refreshes the brightness control. """

		self.brightCtrl.Refresh()


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
		

	def OnSpinCtrl(self, event):
		"""
		Handles the ``wx.EVT_SPINCTRL`` event for RGB and HSB colours.

		:param `event`: a `wx.SpinEvent` event to be processed.
		"""

		obj = event.GetEventObject()
		position = self.spinCtrls.index(obj)
		colourVal = event.GetInt()

		attribute, maxVal = colourAttributes[position], colourMaxValues[position]

		self.AssignColourValue(attribute, colourVal, maxVal, position)
		if self.manualSend:
			pass
		else:
			self.SendLights()

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
			else:
				self._colour.ToRGB()

			self.DrawAll()
			

	def DrawAll(self):
		""" Draws all the custom controls after a colour change. """

		if self._initOver and not self._inDrawAll:
			self._inDrawAll = True

			dc1 = wx.ClientDC(self.hsvBitmap)
			self.hsvBitmap.DrawMarkers(dc1)
			
			dc2 = wx.ClientDC(self.rgbBitmap)
			self.rgbBitmap.DrawMarkers(dc2)
			self.rgbBitmap.DrawLines(dc2)

			dc3 = wx.ClientDC(self.brightCtrl)
			self.brightCtrl.DrawMarkers(dc3)

#			dc4 = wx.ClientDC(self.alphaCtrl)
#			self.alphaCtrl.DrawMarkers(dc4)
			
			self.CalcCuboid()
			self.CalcRects()

			self.DrawRGB()
			self.DrawHSB()
			self.DrawBright()
#			self.DrawAlpha()
			
			self.SetSpinVals()
			self._inDrawAll = False


	def GetColourData(self):
		""" Returns a wxPython compatible `wx.ColourData`. """

		self._colourData.SetColour(self._colour.GetPyColour())
		return self._colourData


	def GetRGBAColour(self):
		""" Returns a 4-elements tuple of red, green, blue, alpha components. """
		# This first gets the color values in RGB
		redcolor=self._colour.r
		greencolor=self._colour.g
		bluecolor=self._colour.b

		# As well as the desired output power level.
		power=self._colour.v
		
		# Calculates the actual power being output at the chosen position as calculated using HSB.
		colorpower=redcolor+greencolor+bluecolor

		# And scales them down so that they have the desired power.
		self._colour.r=redcolor*power/colorpower
		self._colour.g=greencolor*power/colorpower
		self._colour.b=bluecolor*power/colorpower
		self.DrawAll()

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

app = MyApp(redirect=True)
app.MainLoop()

