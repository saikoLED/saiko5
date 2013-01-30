
/******************************************************************************

  Filename:		udpapp.h
  Description:	UDP app for the WiShield 1.0

 ******************************************************************************

  TCP/IP stack and driver for the WiShield 1.0 wireless devices

  Copyright(c) 2009 Async Labs Inc. All rights reserved.

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
  <asynclabs@asynclabs.com>

   Author               Date        Comment
  ---------------------------------------------------------------
   AsyncLabs			07/11/2009	Initial version

 *****************************************************************************/

#include "uip.h"
#include <string.h>
#include "udpapp.h"
#include "config.h"
#include "lo.h"
#include <math.h>

#define redPin 3
#define greenPin 5
#define bluePin 6

#define STATE_INIT				0
#define STATE_LISTENING         1
#define STATE_HELLO_RECEIVED	2
#define STATE_NAME_RECEIVED		3
#define STATE_QUIT 4

static struct udpapp_state s;

void dummy_app_appcall(void)
{
}

void udpapp_init(void)
{
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

static unsigned char parse_msg(void)
{  
  int result = 0;
  int bytes_available = uip_datalen();
  
  unsigned char* pData = uip_appdata;
  
  result = 1;
  
  lo_message message = lo_message_deserialise(pData, bytes_available, &result);
  
  if (result == 0) {
    //char* path = lo_url_get_path(lo_address_get_url(lo_message_get_source(message)));
    lo_arg** argv = lo_message_get_argv(message);
 
    //if (!strcmp(path,'/set/rgb')) {      
      lo_arg* red = argv[0];
      lo_arg* green = argv[1];
      lo_arg* blue = argv[2];  

      float fRed = red->f;
      float fGreen = green->f;
      float fBlue = blue->f;
        
      analogWrite(redPin, (unsigned char)(fRed * 0xFF));
      analogWrite(greenPin, (unsigned char)(fGreen * 0xFF));
      analogWrite(bluePin, (unsigned char)(fBlue * 0xFF));
    /*}
    else if (!strcmp(path, '/set/hsi')) {     
      lo_arg* H = argv[0];
      lo_arg* S = argv[1];
      lo_arg* I = argv[2];  

      unsigned char rgb[3];
      hsi2rgb(H, S, I, rgb);
        
      analogWrite(redPin, rgb[0]);
      analogWrite(greenPin, rgb[1]);
      analogWrite(bluePin, rgb[2]);
    }*/
    
  }
  
  lo_message_free(message);
  s.state = STATE_QUIT;
  return 1;
}

static PT_THREAD(handle_connection(void))
{
	PT_BEGIN(&s.pt);

	s.state = STATE_LISTENING;

	do {
		PT_WAIT_UNTIL(&s.pt, uip_newdata());

		if(uip_newdata() && parse_msg()) {
			uip_flags &= (~UIP_NEWDATA);
		}
        } while (s.state != STATE_QUIT);

	s.state = STATE_INIT;

	PT_END(&s.pt);
}

void udpapp_appcall(void)
{
	handle_connection();
}

void hsi2rgb(float H, float S, float I, int* rgb) {
  float H_rad, H_radm;
  unsigned char r, g, b;
  H = fmod(H,360); // Rotate Hue to be between 0 and 360.
  S = S>0?(S<1?S:1):0; // clamp S and I to interval [0,1]
  I = I>0?(I<1?I:1):0;
    
  if(H < 120) {
    H_rad = H * 0.017453293;
    H_radm = (60-H) * 0.017453293;
    r = 255*I/3*(1+S*cos(H_rad)/cos(H_radm));
    g = 255*I/3*(1+S*(1-cos(H_rad)/cos(H_radm)));
    b = 255*I/3*(1-S);
  } else if(H < 240) {
    H = H - 120;
    H_rad = H * 0.017453293;
    H_radm = (60-H) * 0.017453293;
    g = 255*I/3*(1+S*cos(H_rad)/cos(H_radm));
    b = 255*I/3*(1+S*(1-cos(H_rad)/cos(H_radm)));
    r = 255*I/3*(1-S);
  } else {
    H = H - 240;
    H_rad = H * 0.017453293;
    H_radm = (60-H) * 0.017453293;
    b = 255*I/3*(1+S*cos(H_rad)/cos(H_radm));
    r = 255*I/3*(1+S*(1-cos(H_rad)/cos(H_radm)));
    g = 255*I/3*(1-S);
  }
  rgb[0] = r;
  rgb[1] = g;
  rgb[2] = b;
}
