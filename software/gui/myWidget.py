import wx
from baseColourWidgets import BasePyControl,BaseLineCtrl
from embImages import RGBCubeImage,HSVWheelImage
from custWXUtil import *

########################
#class PowerCtrl(BaseLineCtrl):
#	pass
	
#class XYPanel(BasePyControl):
#	def __init__(self,parent):
#		BasePyControl.__init__(self,parent,RGBCubeImage.GetBitmap())
#		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
#		self.Bind(wx.EVT_MOTION, self.OnMotion)
#		self._leftDown = False
#	def OnLeftUp(self,event):
#		_leftDown = False
#	def OnLeftDown(self,event):
#		_leftDown = True
#		x, y = event.GetX(), event.GetY()
#		size = self.GetSizeTuple()
#		print x,y,size
#		self.GetParent().x = x/size[0]
#		self.GetParent().y = y/size[1]
#	def OnMotion(self,event):
#		if self._leftDown:
#			self.OnLeftDown(event)
#
#
#
class XYPanel(BasePyControl):
    """
    Implements the drawing, mouse handling and sizing routines for the HSV
    colour wheel.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!

        :param `parent`: the control parent window.
        """

        BasePyControl.__init__(self, parent, bitmap=HSVWheelImage.GetBitmap())
        self._mouseIn = False


    def DrawMarkers(self, dc=None):
        """
        Draws the markers on top of the background bitmap.

        :param `dc`: an instance of `wx.DC`.
        """

        if dc is None:
            dc = wx.ClientDC(self)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.WHITE_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(self._mainDialog._currentRect2)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)
        

    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` for L{HSVWheel}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        point = wx.Point(event.GetX(), event.GetY())
        self._mouseIn = False

        if self.InCircle(point):
            self._mouseIn = True

        if self._mouseIn:
            self.CaptureMouse()
            self.TrackPoint(point)


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` for L{HSVWheel}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        if self.GetCapture():
            self.ReleaseMouse()
            self._mouseIn = False


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` for L{HSVWheel}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        point = wx.Point(event.GetX(), event.GetY())

        if self.GetCapture() and self._mouseIn:
            self.TrackPoint(point)
        

    def InCircle(self, pt):
        """
        Returns whether a point is inside the HSV wheel or not.

        :param `pt`: an instance of `wx.Point`.
        """

        return Distance(pt, self._mainDialog._centre2) <= RADIUS


    def TrackPoint(self, pt):
        """
        Track a mouse event inside the HSV colour wheel.

        :param `pt`: an instance of `wx.Point`.
        """

        if not self._mouseIn:
            return

        dc = wx.ClientDC(self)
        self.DrawMarkers(dc)
        mainDialog = self._mainDialog
        colour = mainDialog._colour
                
        colour.t = int(rad2deg(AngleFromPoint(pt, mainDialog._centre2)))
        if colour.t < 0:
            colour.t += 360

        colour.c = int(scaletomax(Distance(pt, mainDialog._centre2)))
        if colour.c > 255:
            colour.c = 255

        mainDialog.CalcRects2()
        mainDialog.CalcRects()
        self.DrawMarkers(dc)
        colour.XYZ_ToRGB_HSV()
        mainDialog.SetSpinVals()
        
        mainDialog.CalcCuboid()
        mainDialog.DrawRGB()
	mainDialog.DrawHSB()
        mainDialog.DrawBright()
        mainDialog.DrawPower()
        mainDialog.DrawAlpha()



import colorsys

class PowerCtrl(BaseLineCtrl):
    """
    Implements the drawing, mouse handling and sizing routines for the brightness
    palette control.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!

        :param `parent`: the control parent window.
        """

        BaseLineCtrl.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        
    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` for L{BrightCtrl}.

        :param `event`: a `wx.PaintEvent` event to be processed.
        """

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        
        colour = self._mainDialog._colour.GetPyColour()
        brightRect = self.BuildRect()
        
        target_red = colour.Red()
        target_green = colour.Green()
        target_blue = colour.Blue()

        h, s, v = colorsys.rgb_to_hsv(target_red / 255.0, target_green / 255.0,
                                      target_blue / 255.0)
        v = 1.0
        vstep = 1.0/(brightRect.height-1)
        
        for y_pos in range(brightRect.y, brightRect.height+brightRect.y):
            r, g, b = [c * 255.0 for c in colorsys.hsv_to_rgb(h, s, v)]
            colour = wx.Colour(int(r), int(g), int(b))
            dc.SetPen(wx.Pen(colour, 1, wx.SOLID))
            dc.DrawRectangle(brightRect.x, y_pos, brightRect.width, 1)
            v = v - vstep

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangleRect(brightRect)
        
        self.DrawMarkers(dc)
        
        
    def TrackPoint(self, pt):
        """
        Tracks a mouse action inside the palette control.

        :param `pt`: an instance of `wx.Point`.
        """

        brightRect = self.BuildRect()
        d = brightRect.GetBottom() - pt.y
        d *= 255
        d /= brightRect.height
        if d < 0:
           d = 0
        if d > 255:
            d = 255;
        
        mainDialog = self._mainDialog
        colour = mainDialog._colour

        mainDialog.DrawMarkers()        
        colour.p = int(d)

        colour.XYZ_ToRGB_HSV()
        mainDialog.SetSpinVals()

        mainDialog.CalcRects()
        mainDialog.CalcRects2()
        mainDialog.CalcCuboid()
        mainDialog.DrawMarkers()
        mainDialog.DrawAlpha()


    def DrawMarkers(self, dc=None):
        """
        Draws square markers used with mouse gestures.

        :param `dc`: an instance of `wx.DC`.
        """

        if dc is None:
            dc = wx.ClientDC(self)
            
        colour = self._mainDialog._colour
        brightRect = self.BuildRect()
        
        y = int(colour.p/255.0*brightRect.height)
        y = brightRect.GetBottom() - y
        brightMark = wx.Rect(brightRect.x-2, y-4, brightRect.width+4, 8)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(brightMark)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)
