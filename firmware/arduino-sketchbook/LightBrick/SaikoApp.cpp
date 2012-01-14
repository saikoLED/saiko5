
/*
  SaikoApp.cpp
  LightBrick Wireless Shield Control Code
  Copyright(c) 2011 SaikoLED. All rights reserved.

  Based on udpapp.h: TCP/IP stack and driver for the WiShield 1.0 wireless devices
  Copyright(c) 2009 Asynclabs Inc. All rights reserved.

  This program is free software; you can redistribute it and/or modify it
  under the terms of version 2 of the GNU General Public License as
  published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
  more details.

  You should have received a copy of the GNU General Public License along with
  this program; if not, write to the Free Software Foundation, Inc., 59
  Temple Place - Suite 330, Boston, MA  02111-1307, USA.

  Contact Information:
  <dan@saikoled.com>
  <asynclabs@asynclabs.com>

   Author                       Date            Comment
  ---------------------------------------------------------------
   SaikoLED                     01/08/2011      Convert to CPP, add OSC
   AsyncLabs			07/11/2009      Initial version

 *****************************************************************************/
extern "C" {
#include "uip.h"
}

#include "udpapp.h"
#include "config.h"
#include "SaikoColor.h"

void respondToOSC(int argc, lo_arg** argv, String msg_path,
                    int &outEnable, char &outputModes);


#define DEBUG 0

#define redPin 3
#define greenPin 5
#define bluePin 6

#define STATE_INIT				0
#define STATE_LISTENING         1
#define STATE_HELLO_RECEIVED	2
#define STATE_NAME_RECEIVED		3
#define STATE_QUIT 4

static struct udpapp_state s;

bool smoothingMode(char bits) {return (bits & (1<<1));} //replace with byte for 8 toggles..
bool velocityMode(char bits) {return (bits & (1<<2));}
bool recordMode(char bits) {return (bits & (1<<3));}
bool fullBrightMode(char bits) {return (bits & (1<<4));}

static unsigned char parse_msg(void)
{

  int result = 0;
  int bytes_available = uip_datalen();
  unsigned char* pData = (unsigned char*)uip_appdata;
  int outEnable = 0;
  
  result = 1;
  
  lo_message message = lo_message_deserialise(pData, bytes_available, &result);
  char modes =0;
  if (result == 0) {
    lo_arg** argv = lo_message_get_argv(message);
    int argc = lo_message_get_argc(message);
    String msg_path = lo_get_path(pData,bytes_available);
    respondToOSC(argc,argv,msg_path,outEnable,modes);
    //nextScriptStep(&outEnable); //should set outEnable to true if more steps
  }
  if (outEnable) {
      if (fullBrightMode(modes)) {
        Serial.println("fullbright");
        color.fI = 1;
        hsi2rgb(&color);
      }    
      analogWrite(redPin, (unsigned char)(color.fRed * 0xFF));
      analogWrite(greenPin, (unsigned char)(color.fGreen * 0xFF));
      analogWrite(bluePin, (unsigned char)(color.fBlue * 0xFF));

  }
  
  lo_message_free(message);
  s.state = STATE_QUIT;
  return(1);
}

void respondToOSC(int argc, lo_arg** argv, String msg_path,
                    int &outEnable, char &outputModes)
  {
  size_t pos;
  lo_arg *val1,*val2,*val3,*val4;
  char test;

  if (DEBUG)
    Serial.println(msg_path);
  /* switch by number of arguments to handle, then pathname */
  switch (argc) {
        case 0:
          break;
        case 1:
          pos = msg_path.indexOf('/fader');
          if (pos != -1) {
            outEnable = 1;
            val1 = argv[0];
            test = msg_path[pos+1]; //maybe need a case for '\0' ->white fade
            if (test=='1') {
              color.fRed = val1->f;
              rgb2hsi(&color); 
              }
            else if (test=='2') {
              color.fGreen = val1->f;
              rgb2hsi(&color); 
              }
            else if (test=='3') {
              color.fBlue = val1->f;
              rgb2hsi(&color); 
              }
            else if (test=='4') {
              color.fI = val1->f;
              hsi2rgb(&color); 
              }
            else if (test=='5') {
              color.fS = val1->f;
              hsi2rgb(&color); 
              }
            else if (test=='6') {
              color.fH = 360.0 * val1->f;
              hsi2rgb(&color); 
              }
            else
              color.fGreen=1;
          }
          else {
           pos = msg_path.indexOf('/toggle');
           if (pos != -1) {
             val1 = argv[0];
             test = msg_path[pos+1]; //maybe need a case for '\0' ->white fade

             if (test=='1')
               outputModes ^= (0.0 < val1->f) << 1;
             if (test=='2')
               outputModes ^= (0.0 < val1->f) << 2;
             if (test=='3')
               outputModes ^= (0.0 < val1->f) << 3;
             if (test=='4')
               outputModes ^= (0.0 < val1->f) << 4;
           }
          }
          break;
        case 2:
          pos = msg_path.indexOf('/xy');
          //if (DEBUG)
          // Serial.println(pos);
          if (pos != -1) {
            outEnable = 1;
            test = msg_path[pos+1]; 
            if (test == '\0'){
              color.fS = argv[0]->f;
              color.fH = (argv[1]->f)*360;
              hsi2rgb(&color);
            }
          }
          break;
        case 5:
        case 4:  
        case 3:
           val1 = argv[0];
           val2 = argv[1];
           val3 = argv[2];  
           if (msg_path.indexOf('/set/rgb') != -1)
           {
               color.fRed = val1->f;
               color.fGreen = val2->f;
               color.fBlue = val3->f;
               rgb2hsi(&color); 
           } 
           else if (msg_path.indexOf('/set/hsi') != -1)
           {
               color.fH = val1->f*360;
               color.fS = val2->f;
               color.fI = val3->f;
               hsi2rgb(&color);
            } 
            else { //legacy support, remove in future version
            
              if (DEBUG)
                Serial.println("missing path, assume RGB");
              if ((msg_path == NULL) || (msg_path[0] != '/'))
                 break;
              color.fRed = val1->f;
              color.fGreen = val2->f;
              color.fBlue = val3->f;
              rgb2hsi(&color); 
          }
          outEnable = 1;
          break;
  
        } //end switch
  } //end respondToOSC
  
  
static PT_THREAD(handle_connection(void))
{
	PT_BEGIN(&s.pt);

	s.state = STATE_LISTENING;

	do {
		PT_WAIT_UNTIL(&s.pt, uip_newdata());

		if(uip_newdata() && parse_msg()) {
//			s.state = STATE_HELLO_RECEIVED;
			uip_flags &= (~UIP_NEWDATA);
//			break;
		}
//	} while(s.state != STATE_HELLO_RECEIVED);
        } while (s.state != STATE_QUIT);

//	do {
//		send_request();
//		PT_WAIT_UNTIL(&s.pt, uip_newdata());
//
//		if(uip_newdata()) {
//			s.state = STATE_NAME_RECEIVED;
//			uip_flags &= (~UIP_NEWDATA);
//			break;
//		}
//	} while(s.state != STATE_NAME_RECEIVED);

//	send_response();

	s.state = STATE_INIT;

	PT_END(&s.pt);
}

extern "C" {
  void dummy_app_appcall(void)
  {
  }

  void udpapp_init(void)
  {
    
        color.fRed = 0;
        color.fGreen = 0;
        color.fBlue = 0;
        rgb2hsi(&color);
        if (DEBUG)
        {
          Serial.begin(115200);
  	  Serial.println("hi there");
        }
        uip_ipaddr_t addr;
  	struct uip_udp_conn *c;
  
  	uip_ipaddr(&addr, 255, 255, 255, 255);
  	c = uip_udp_new(&addr, HTONS(0));
  	if(c != NULL) {
  		uip_udp_bind(c, HTONS(2222));
  	}
  
  	s.state = STATE_INIT;
  
  	PT_INIT(&s.pt);
  }
  void udpapp_appcall(void)
  {
	handle_connection();
  }
}


