
/*
  udpapp.cpp
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
#include <string.h>
#include "udpapp.h"
#include "config.h"
#include "lo.h"
#include "hsi2rgb.h"
#include "WProgram.h"
#define DEBUG 1

#define redPin 3
#define greenPin 5
#define bluePin 6

#define STATE_INIT				0
#define STATE_LISTENING         1
#define STATE_HELLO_RECEIVED	2
#define STATE_NAME_RECEIVED		3
#define STATE_QUIT 4

t_hsi2rgb color;
static struct udpapp_state s;
bool smoothingMode = false; //replace with byte for 8 toggles..
bool velocityMode = false; //replace with byte for 8 toggles..
bool recordMode = false; //replace with byte for 8 toggles..
bool fullBrightMode = false; //replace with byte for 8 toggles..

static unsigned char parse_msg(void)
{

  int result = 0;
  int bytes_available = uip_datalen();
  unsigned char* pData = (unsigned char*)uip_appdata;

  result = 1;
  int outEnable = 0;

  lo_message message = lo_message_deserialise(pData, bytes_available, &result);
  
  if (result == 0) {
    lo_arg** argv = lo_message_get_argv(message);
    int argc = lo_message_get_argc(message);
    lo_arg *red,*green,*blue,*val1,*val2;
    char test;
    size_t pos;
    String msg_path(lo_get_path(pData,bytes_available));
    if (DEBUG)
      Serial.println(msg_path);
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
           Serial.println(val1->f);
           if (test=='1')
             smoothingMode = (0.0 < val1->f);
           if (test=='2')
             velocityMode = (0.0 < val1->f);
           if (test=='3')
             recordMode = (0.0 < val1->f);
           if (test=='4')
             fullBrightMode = (0.0 < val1->f);
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
        if ((msg_path == NULL) || (msg_path[0] != '/'))
           break;
        if ((msg_path[1] != 'l') && (msg_path[1] != 'L'))
           break;
        red = argv[0];
        green = argv[1];
        blue = argv[2];  
        color.fRed = red->f;
        color.fGreen = green->f;
        color.fBlue = blue->f;
        outEnable = 1;
        break;

      }
  }
  if (outEnable) {
      if (fullBrightMode) {
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

//static void send_request(void)
//{
//	char str[] = "Hello. What is your name?\n";
//
//	memcpy(uip_appdata, str, strlen(str));
//	uip_send(uip_appdata, strlen(str));
//}

//static void send_response(void)
//{
//	char i = 0;
//	char str[] = "Hello ";
//
//	while ( ( ((char*)uip_appdata)[i] != '\n') && i < 9) {
//		s.inputbuf[i] = ((char*)uip_appdata)[i];
//		i++;
//	}
//	s.inputbuf[i] = '\n';
//
//	memcpy(uip_appdata, str, 6);
//	memcpy(uip_appdata+6, s.inputbuf, i+1);
//	uip_send(uip_appdata, i+7);
//}

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


