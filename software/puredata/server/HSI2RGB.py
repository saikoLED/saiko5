import math

def convert(H, S, I):
    if H < 120:
        R = I/3*(1+S*math.cos(math.radians(H))/math.cos(math.radians(60-H)))
        G = I/3*(1+S*(1-math.cos(math.radians(H))/math.cos(math.radians(60-H))))
        B = I/3*(1-S)
    elif H < 240:
        H = H - 120
        G = I/3*(1+S*math.cos(math.radians(H))/math.cos(math.radians(60-H)))
        B = I/3*(1+S*(1-math.cos(math.radians(H))/math.cos(math.radians(60-H))))
        R = I/3*(1-S)
    else:
        H = H - 240
        B = I/3*(1+S*math.cos(math.radians(H))/math.cos(math.radians(60-H)))
        R = I/3*(1+S*(1-math.cos(math.radians(H))/math.cos(math.radians(60-H))))
        G = I/3*(1-S)
    return [R, G, B]

