/*
 Fading
 
 This example shows how to fade an LED using the analogWrite() function.
 
 The circuit:
 * LED attached from digital pin 9 to ground.
 
 Created 1 Nov 2008
 By David A. Mellis
 Modified 17 June 2009
 By Tom Igoe
 
 http://arduino.cc/en/Tutorial/Fading
 
 */
 
#include "math.h"
#define DEG_TO_RAD(X) (M_PI*(X)/180)

#define ontime 20 // Delay time between incrementing PWM.
#define offtime 100 //
#define steptime 1
#define fadestep 10
#define redPin 3    // Red LED connected to digital pin 9
#define greenPin 5 // Green LED connected to digital pin 10
#define bluePin 6 // Blue LED connected to digital pin 11

struct HSI {
  float h;
  float s;
  float i;
} color;

void sendcolor() {
  int rgb[3];
  while (color.h >=360) color.h = color.h - 360;
  while (color.h < 0) color.h = color.h + 360;
  if (color.i > 1) color.i = 1;
  if (color.i < 0) color.i = 0;
  if (color.s > 1) color.s = 1;
  if (color.s < 0) color.s = 0;
  // Fix ranges.
  hsi2rgb(color.h, color.s, color.i, rgb);
  analogWrite(redPin, rgb[0]);
  analogWrite(greenPin, rgb[1]);
  analogWrite(bluePin, rgb[2]);
}

void setup()  {
  color.h = 0;
  color.s = 1;
  color.i = 0;
  // Initial color = off, hue of red fully saturated.
  while (color.i < 1) {
    sendcolor();
    color.i = color.i + 0.0002; // Increase Intensity
    color.h = color.h + 0.01; // Rotate Hue
    delay (steptime);
  }
} 

void loop()  {
  sendcolor();
  color.h = color.h + 0.01;
  delay (steptime);
}

void hsi2rgb(float H, float S, float I, int* rgb) {
  int r, g, b;
  H = fmod(H,360); // cycle H around to 0-360 degrees
  H = 3.14159*H/(float)180; // Convert to radians.
  S = S>0?(S<1?S:1):0; // clamp S and I to interval [0,1]
  I = I>0?(I<1?I:1):0;
    
  if(H < 2.09439) {
    r = 255*I/3*(1+S*cos(H)/cos(1.047196667-H));
    g = 255*I/3*(1+S*(1-cos(H)/cos(1.047196667-H)));
    b = 255*I/3*(1-S);
  } else if(H < 4.188787) {
    H = H - 2.09439;
    g = 255*I/3*(1+S*cos(H)/cos(1.047196667-H));
    b = 255*I/3*(1+S*(1-cos(H)/cos(1.047196667-H)));
    r = 255*I/3*(1-S);
  } else {
    H = H - 4.188787;
    b = 255*I/3*(1+S*cos(H)/cos(1.047196667-H));
    r = 255*I/3*(1+S*(1-cos(H)/cos(1.047196667-H)));
    g = 255*I/3*(1-S);
  }
  rgb[0]=r;
  rgb[1]=g;
  rgb[2]=b;
}
