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

int delaytime = 5; // Delay time between incrementing PWM.
int fadestep = 1;
int redPin = 3;    // Red LED connected to digital pin 9
int greenPin = 5; // Green LED connected to digital pin 10
int bluePin = 6; // Blue LED connected to digital pin 11

void setup()  {
  for(int fadeValue = 0 ; fadeValue <= 255; fadeValue += fadestep) { 
    // sets the value (range from 0 to 255):
    analogWrite(redPin, fadeValue);    
    delayMicroseconds(delaytime);                            
  }
} 

void loop()  {
  for(int fadeValue = 0 ; fadeValue <= 255; fadeValue += fadestep) { 
    // sets the value (range from 0 to 255):
    analogWrite(redPin, 255-fadeValue);
    analogWrite(greenPin, fadeValue);   
    delay(delaytime);                            
  }
  
  for(int fadeValue = 0 ; fadeValue <= 255; fadeValue += fadestep) { 
    // sets the value (range from 0 to 255):
    analogWrite(greenPin, 255-fadeValue);
    analogWrite(bluePin, fadeValue); 
    delay(delaytime);                            
  }
  
  for(int fadeValue = 0 ; fadeValue <= 255; fadeValue += fadestep) { 
    // sets the value (range from 0 to 255):
    analogWrite(bluePin, 255-fadeValue);
    analogWrite(redPin, fadeValue); 
    delay(delaytime);                            
  }
//  digitalWrite(greenPin, HIGH);
//  delay(1000);
//  digitalWrite(greenPin, LOW);
//  delay(1000);
}


