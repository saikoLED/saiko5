#include <math.h>
#define DEG_TO_RAD(X) (M_PI*(X)/180)
#define M_PI 3.14159

/* all on scale of 0 to 1.0 except hue: 0->360 */
typedef struct _hsi2rgb {
  float fH,fS,fI;
  float fRed,fGreen,fBlue;
} t_hsi2rgb;

void hsi2rgb(t_hsi2rgb *x) {

  // do the conversion
  float r,g,b;
  float H, S, I;
  H = x->fH;
  S = x->fS;
  I = x->fI;

  H = fmod(H,360);
  S = S>0?(S<1?S:1):0; // clamp S and I to interval [0,1]
  I = I>0?(I<1?I:1):0;
    
  if(H < 120) {
    r = I/3*(1+S*cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H)));
    g = I/3*(1+S*(1-cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H))));
    b = I/3*(1-S);
  } else if(H < 240) {
    H = H - 120;
    g = I/3*(1+S*cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H)));
    b = I/3*(1+S*(1-cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H))));
    r = I/3*(1-S);
  } else {
    H = H - 240;
    b = I/3*(1+S*cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H)));
    r = I/3*(1+S*(1-cos(DEG_TO_RAD(H))/cos(DEG_TO_RAD(60-H))));
    g = I/3*(1-S);
  }

  // now output
  x->fRed = r;
  x->fGreen = g;
  x->fBlue = b;
}

void rgb2hsi(t_hsi2rgb *x)
{
	float &R = (x->fRed);
	float &G = (x->fGreen);
	float &B = (x->fBlue);
	float &H = (x->fH);
	float &S = (x->fS);
	float &I = (x->fI);

	float minv = R;
	if (G < minv)
		minv = G;
	if (B < minv)
		minv = B;

	I = (R+G+B)/3.0;
	S = 1 - minv/I;
	if (S == 0.0)
	{
		H = 0.0;
        }
	else
	{
		H = ((R-G)+(R-B))/2.0;
		H = H/sqrt((R-G)*(R-G) + (R-B)*(G-B));
		H = acos(H);
		if (B > G)
		{
			H = 2.0*M_PI - H;
		}
		H = 360.0*H/(2.0*M_PI);
	}
}
