from math import pi, sin, cos, sqrt, atan2
import wx



# Radius of the HSB colour wheel
RADIUS = 100
""" Radius of the HSB colour wheel. """

# Width of the mouse-controlled colour pointer
RECT_WIDTH = 5
""" Width of the mouse-controlled colour pointer. """

# Dictionary keys for the RGB colour cube
RED, GREEN, BLUE = 0, 1, 2
""" Dictionary keys for the RGB colour cube. """

Vertex = wx.Point(95, 109)
Top = wx.Point(95, 10)
Left = wx.Point(16, 148)
Right = wx.Point(174, 148)

def RestoreOldDC(dc, oldPen, oldBrush, oldMode):
    """
    Restores the old settings for a `wx.DC`.

    :param `dc`: an instance of `wx.DC`;
    :param `oldPen`: an instance of `wx.Pen`;
    :param `oldBrush`: an instance of `wx.Brush`;
    :param `oldMode`: the `wx.DC` drawing mode bit.
    """

    dc.SetPen(oldPen)
    dc.SetBrush(oldBrush)
    dc.SetLogicalFunction(oldMode)


def rad2deg(x):
    """
    Transforms radians into degrees.

    :param `x`: a float representing an angle in radians.    
    """
    
    return 180.0*x/pi

def deg2rad(x):
    """
    Transforms degrees into radians.

    :param `x`: a float representing an angle in degrees.    
    """

    return x*pi/180.0

def toscale(x):
    """
    Normalize a value as a function of the radius.

    :param `x`: a float value to normalize    
    """ 

    return x*RADIUS/255.0

def scaletomax(x):
    """
    Normalize a value as a function of the radius.

    :param `x`: a float value to normalize    
    """ 

    return x*255.0/RADIUS

def rgb2html(colour):
    """
    Transforms a RGB triplet into an html hex string.

    :param `colour`: a tuple of red, green, blue integers.
    """

    hexColour = "#%02x%02x%02x"%(colour.r, colour.g, colour.b)
    return hexColour.upper()

    
def Slope(pt1, pt2):
    """
    Calculates the slope of the line connecting 2 points.

    :param `pt1`: an instance of `wx.Point`;
    :param `pt2`: another instance of `wx.Point`.
    """

    y = float(pt2.y - pt1.y)
    x = float(pt2.x - pt1.x)

    if x:
        return y/x
    else:
        return None


def Intersection(line1, line2):
    """
    Calculates the intersection point between 2 lines.

    :param `line1`: an instance of L{LineDescription};
    :param `line2`: another instance of L{LineDescription}.
    """

    if line1.slope == line2.slope:
    
        # Parallel lines, no intersection
        return wx.Point(0, 0)
    
    elif line1.slope is None:
    
        # First Line is vertical, eqn is x=0
        # Put x = 0 in second line eqn to get y
        x = line1.x
        y = line2.slope*x + line2.c
    
    elif line2.slope is None:
    
        # second line is vertical Equation of line is x=0
        # Put x = 0 in first line eqn to get y
        x = line2.x
        y = line1.slope*line2.x + line1.c
    
    else:
    
        y = ((line1.c*line2.slope) - (line2.c*line1.slope))/(line2.slope - line1.slope)
        x = (y - line1.c)/line1.slope
    

    return wx.Point(int(x), int(y))


def FindC(line):
    """ Internal function. """

    if line.slope is None:
        c = line.y
    else:
        c = line.y - line.slope*line.x
    
    return c


def PointOnLine(pt1, pt2, length, maxLen):
    """ Internal function. """

    a = float(length)

    if pt2.x != pt1.x:
    
        m = float((pt2.y - pt1.y))/(pt2.x - pt1.x)
        m2 = m*m
        a2 = a*a
        c = pt1.y - m*pt1.x
        c2 = c*c

        A = 1.0
        
        x = pt1.x

        B = 2.0 * pt1.x

        x *= x
        C = x - a2/(m2 + 1)
        
        x = (B + sqrt(B*B - (4.0*A*C)))/(2.0*A)
        y = m*x + c
        pt = wx.Point(int(x), int(y))

        if Distance(pt, pt1) > maxLen or Distance(pt, pt2) > maxLen:
        
            x = (B - sqrt(B*B - (4.0*A*C)))/(2.0*A)
            y = m*x + c
            pt = wx.Point(int(x), int(y))
        
    else:
    
        a2 = a*a
        y = sqrt(a2)
        x = 0.0
        pt = wx.Point(int(x), int(y))
        pt.x += pt1.x
        pt.y += pt1.y
        
        if Distance(pt, pt1) > maxLen or Distance(pt, pt2) > maxLen:

            y = -1.0*y        
            pt = wx.Point(int(x), int(y))
            pt.x += pt1.x
            pt.y += pt1.y
    
    return pt


def Distance(pt1, pt2):
    """
    Returns the distance between 2 points.

    :param `pt1`: an instance of `wx.Point`;
    :param `pt2`: another instance of `wx.Point`.    
    """

    distance = sqrt((pt1.x - pt2.x)**2.0 + (pt1.y - pt2.y)**2.0)
    return int(distance)


def AngleFromPoint(pt, center):
    """
    Returns the angle between the x-axis and the line connecting the center and
    the point `pt`.

    :param `pt`: an instance of `wx.Point`;
    :param `center`: a float value representing the center.
    """

    y = -1*(pt.y - center.y)
    x = pt.x - center.x
    if x == 0 and y == 0:
    
        return 0.0
    
    else:
    
        return atan2(y, x)
    

def PtFromAngle(angle, sat, center):
    """
    Given the angle with respect to the x-axis, returns the point based on
    the saturation value.

    :param `angle`: a float representing an angle;
    :param `sat`: a float representing the colour saturation value;
    :param `center`: a float value representing the center.
    """

    angle = deg2rad(angle)
    sat = toscale(sat)

    x = sat*cos(angle)
    y = sat*sin(angle)

    pt = wx.Point(int(x), -int(y))
    pt.x += center.x
    pt.y += center.y
    
    return pt
