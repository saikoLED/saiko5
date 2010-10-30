import wx


class BasePyControl(wx.PyControl):
    """
    Base class used to hold common code for the HSB colour wheel and the RGB
    colour cube.
    """

    def __init__(self, parent, bitmap=None):
        """
        Default class constructor.
        Used internally. Do not call it in your code!

        :param `parent`: the control parent;
        :param `bitmap`: the background bitmap for this custom control.
        """

        wx.PyControl.__init__(self, parent, style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self._bitmap = bitmap
        mask = wx.Mask(self._bitmap, wx.Colour(192, 192, 192))
        self._bitmap.SetMask(mask)
        
        self._mainDialog = wx.GetTopLevelParent(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` for L{BasePyControl}.

        :param `event`: a `wx.PaintEvent` event to be processed.
        """

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        
        dc.Clear()
        dc.DrawBitmap(self._bitmap, 0, 0, True)

        if self._mainDialog._initOver:
            self.DrawMarkers(dc)
        

    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` for L{BasePyControl}.

        :param `event`: a `wx.EraseEvent` event to be processed.

        :note: This is intentionally empty to reduce flicker.        
        """

        pass

    
    def DrawMarkers(self, dc=None):
        """
        Draws the markers on top of the background bitmap.

        :param `dc`: an instance of `wx.DC`.
        
        :note: This method must be overridden in derived classes.
        """

        pass


    def DrawLines(self, dc):
        """
        Draws the lines connecting the markers on top of the background bitmap.

        :param `dc`: an instance of `wx.DC`.
        
        :note: This method must be overridden in derived classes.
        """

        pass
    

    def AcceptsFocusFromKeyboard(self):
        """
        Can this window be given focus by keyboard navigation? If not, the
        only way to give it focus (provided it accepts it at all) is to click
        it.

        :note: This method always returns ``False`` as we do not accept focus from
         the keyboard.

        :note: Overridden from `wx.PyControl`.
        """

        return False


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        :note: This method always returns ``False`` as we do not accept focus from
         mouse click.

        :note: Overridden from `wx.PyControl`.
        """

        return False

    
    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` for L{BasePyControl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        
        :note: This method must be overridden in derived classes.
        """

        pass


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` for L{BasePyControl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        
        :note: This method must be overridden in derived classes.
        """

        pass


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` for L{BasePyControl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        
        :note: This method must be overridden in derived classes.
        """

        pass
    
    
    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` for L{BasePyControl}.

        :param `event`: a `wx.SizeEvent` event to be processed.        
        """

        self.Refresh()
        

    def DoGetBestSize(self):
        """ Returns the custom control best size (used by sizers). """

        return wx.Size(self._bitmap.GetWidth(), self._bitmap.GetHeight())        




class BaseLineCtrl(wx.PyControl):
    """
    Base class used to hold common code for the Alpha channel control and the
    brightness palette control.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!

        :param `parent`: the control parent window.
        """

        wx.PyControl.__init__(self, parent, size=(20, 200), style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)    

        self._mainDialog = wx.GetTopLevelParent(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` for L{BaseLineCtrl}.

        :param `event`: a `wx.EraseEvent` event to be processed.

        :note: This is intentionally empty to reduce flicker.        
        """

        pass


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` for L{BaseLineCtrl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        point = wx.Point(event.GetX(), event.GetY())
        theRect = self.GetClientRect()

        if not theRect.Contains(point):
            event.Skip()
            return

        self.CaptureMouse()
        self.TrackPoint(point)


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` for L{BaseLineCtrl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        if self.GetCapture():
            self.ReleaseMouse()


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` for L{BaseLineCtrl}.

        :param `event`: a `wx.MouseEvent` event to be processed.
        """

        point = wx.Point(event.GetX(), event.GetY())

        if self.GetCapture():
            self.TrackPoint(point)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` for L{BaseLineCtrl}.

        :param `event`: a `wx.SizeEvent` event to be processed.
        """

        self.Refresh()


    def DoGetBestSize(self):
        """ Returns the custom control best size (used by sizers). """

        return wx.Size(24, 208)    


    def BuildRect(self):
        """ Internal method. """

        brightRect = wx.Rect(*self.GetClientRect())
        brightRect.x += 2
        brightRect.y += 6
        brightRect.width -= 4
        brightRect.height -= 8

        return brightRect


    def AcceptsFocusFromKeyboard(self):
        """
        Can this window be given focus by keyboard navigation? If not, the
        only way to give it focus (provided it accepts it at all) is to click
        it.

        :note: This method always returns ``False`` as we do not accept focus from
         the keyboard.

        :note: Overridden from `wx.PyControl`.
        """

        return False


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click? 

        :note: This method always returns ``False`` as we do not accept focus from
         mouse click.

        :note: Overridden from `wx.PyControl`.
        """

        return False



