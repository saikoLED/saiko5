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
 
#include <math.h>
#define DEG_TO_RAD(X) (M_PI*(X)/180)

#define ontime 20 // Delay time between incrementing PWM.
#define offtime 100 // 
#define fadestep 10
#define redPin 3    // Red LED connected to digital pin 9
#define greenPin 5 // Green LED connected to digital pin 10
#define bluePin 6 // Blue LED connected to digital pin 11

float previous_hue;

void setup()  {
} 

void loop()  {
  int rgb[3];
  float hue = random(previous_hue+15, previous_hue + 330);
  float saturation = 1;
  float intensity = 1;
  hsi2rgb(hue, saturation, intensity, rgb);
  analogWrite(redPin, rgb[0]);
  analogWrite(greenPin, rgb[1]);
  analogWrite(bluePin, rgb[2]);
  delay(ontime);
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
  delay(offtime);
  previous_hue = hue;
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
  
  
