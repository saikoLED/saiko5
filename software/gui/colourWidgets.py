import wx
#from wx.lib.embeddedimage import PyEmbeddedImage
from custWXUtil import *
from baseColourWidgets import BasePyControl,BaseLineCtrl
from embImages import RGBCubeImage,HSVWheelImage


class RGBCube(BasePyControl):
    """
    Implements the drawing, mouse handling and sizing routines for the RGB
    cube colour.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!

        :param `parent`: the control parent window.        
        """

        BasePyControl.__init__(self, parent, bitmap=RGBCubeImage.GetBitmap())
        self._index = -1


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

        rects = []
        blueLen = self._mainDialog._blueLen
        greenLen = self._mainDialog._greenLen
        redLen = self._mainDialog._redLen
        colour = self._mainDialog._colour

        pt = [wx.Point() for i in xrange(3)]
        pt[0] = PointOnLine(Vertex, Top, (colour.r*redLen)/255, redLen)
        pt[1] = PointOnLine(Vertex, Left, (colour.g*greenLen)/255, greenLen)
        pt[2] = PointOnLine(Vertex, Right, (colour.b*blueLen)/255, blueLen)

        for i in xrange(3):
            rect = wx.Rect(pt[i].x - RECT_WIDTH, pt[i].y - RECT_WIDTH, 2*RECT_WIDTH, 2*RECT_WIDTH)
            rects.append(rect)
            dc.DrawRectangleRect(rect)

        self.DrawLines(dc)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)

        self._rects = rects
        

    def DrawLines(self, dc):
        """
        Draws the lines connecting the markers on top of the background bitmap.

        :param `dc`: an instance of `wx.DC`.
        """
        
        cuboid = self._mainDialog._cuboid
        
        dc.DrawLinePoint(cuboid[1], cuboid[2])
        dc.DrawLinePoint(cuboid[2], cuboid[3])
        dc.DrawLinePoint(cuboid[3], cuboid[4])
        dc.DrawLinePoint(cuboid[4], cuboid[5])
        dc.DrawLinePoint(cuboid[5], cuboid[2])

        dc.DrawLinePoint(cuboid[5], cuboid[6])
        dc.DrawLinePoint(cuboid[6], cuboid[7])
        dc.DrawLinePoint(cuboid[7], cuboid[4])

        dc.DrawLinePoint(cuboid[1], cuboid[6])
        

    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` for L{RGBCube}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """
        
        point = wx.Point(event.GetX(), event.GetY())
        self._mouseIn = False

        if self._rects[RED].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = RED
        
        elif self._rects[GREEN].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = GREEN
        
        elif self._rects[BLUE].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = BLUE

        
    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` for L{RGBCube}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """
        
        if self.GetCapture():
            self.ReleaseMouse()
            self._mouseIn = False
        

    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` for L{RGBCube}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """
        
        point = wx.Point(event.GetX(), event.GetY())
        
        if not (self.GetCapture() and self._mouseIn):
            event.Skip()
            return

        bChange = False
        mainDialog = self._mainDialog
        colour = mainDialog._colour
        redLen, greenLen, blueLen = mainDialog._redLen, mainDialog._greenLen, mainDialog._blueLen

        dc = wx.ClientDC(self)
        self.DrawMarkers(dc)
        
        if self._index == RED:
        
            if point.y > Vertex.y:          
                point.y = Vertex.y
            
            point.x = Vertex.x
            val = Distance(point, Vertex)
            if val > redLen:
                val = redLen
            
            val = (float(val)/redLen)*255
            colour.r = int(val)

            pt = PointOnLine(Vertex, Top, (colour.r*redLen)/255, redLen)
            self._rects[RED] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                       2*RECT_WIDTH, 2*RECT_WIDTH)

            bChange = True
        
        elif self._index == GREEN:
        
            if point.x > Vertex.x:          
                point.x = Vertex.x
            
            point.y = self._rects[GREEN].GetTop() + RECT_WIDTH
            val = Distance(point, Vertex)
            if val > greenLen:
                val = greenLen
            
            val = (float(val)/greenLen)*255
            colour.g = int(val)

            pt = PointOnLine(Vertex, Left, (colour.g*greenLen)/255, greenLen)
            self._rects[GREEN] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                         2*RECT_WIDTH, 2*RECT_WIDTH)

            bChange = True
        
        elif self._index == BLUE:
        
            if point.x < Vertex.x:
                point.x = Vertex.x

            point.y = self._rects[BLUE].GetTop() + RECT_WIDTH
            val = Distance(point, Vertex)
            if val > blueLen:
                val = blueLen
            
            val = (float(val)/blueLen)*255
            colour.b = int(val)

            pt = PointOnLine(Vertex, Right, (colour.b*blueLen)/255, blueLen)
            self._rects[BLUE] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                        2*RECT_WIDTH, 2*RECT_WIDTH)
            
            bChange = True
        
        if bChange:

            mainDialog.CalcCuboid()
            self.DrawMarkers(dc)
        
            colour.ToHSV()
            mainDialog.SetSpinVals()
            mainDialog.CalcRects()
            mainDialog.CalcRects2()

            mainDialog.DrawHSB()
		
	    #really should be done from maindialog itself to preserve abstraction
            mainDialog.DrawXYZ()
            mainDialog.DrawBright()
            mainDialog.DrawPower()
            mainDialog.DrawAlpha()


class HSVWheel(BasePyControl):
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
        
        dc.DrawRectangleRect(self._mainDialog._currentRect)
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

        return Distance(pt, self._mainDialog._centre) <= RADIUS


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
                
        colour.h = int(rad2deg(AngleFromPoint(pt, mainDialog._centre)))
        if colour.h < 0:
            colour.h += 360

        colour.s = int(scaletomax(Distance(pt, mainDialog._centre)))
        if colour.s > 255:
            colour.s = 255

        mainDialog.CalcRects()
        mainDialog.CalcRects2()
        self.DrawMarkers(dc)
        colour.ToRGB()
        mainDialog.SetSpinVals()
        
        mainDialog.CalcCuboid()
        mainDialog.DrawRGB()
        mainDialog.DrawXYZ()
        mainDialog.DrawBright()
        mainDialog.DrawPower()
        mainDialog.DrawAlpha()


import colorsys
class BrightCtrl(BaseLineCtrl):
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
        colour.v = int(d)

        colour.ToRGB()
        mainDialog.SetSpinVals()

        mainDialog.CalcRects()
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
        
        y = int(colour.v/255.0*brightRect.height)
        y = brightRect.GetBottom() - y
        brightMark = wx.Rect(brightRect.x-2, y-4, brightRect.width+4, 8)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(brightMark)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)
