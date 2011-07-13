#include "m_pd.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define DEG_TO_RAD(X) (M_PI*(X)/180)

static t_class *hsi2rgb_class;

typedef struct _hsi2rgb {
  t_object x_obj;
  t_float i_h, i_s, i_i;
  t_outlet *o_r;
  t_outlet *o_g;
  t_outlet *o_b;
} t_hsi2rgb;

void hsi2rgb_float(t_hsi2rgb *x, t_floatarg h) {
  // save h for later, so bang does right thing
  x->i_h = h;

  // do the conversion
  t_float r,g,b;
  t_float H, S, I;
  H = x->i_h;
  S = x->i_s;
  I = x->i_i;

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
  outlet_float(x->o_r, r);
  outlet_float(x->o_g, g);
  outlet_float(x->o_b, b);
}

void hsi2rgb_bang(t_hsi2rgb *x) {
  hsi2rgb_float(x, x->i_h);
}

void hsi2rgb_free(t_hsi2rgb *x) {
  // well, it's being freed.
}

void * hsi2rgb_new(void) {
  t_hsi2rgb *x = (t_hsi2rgb*)pd_new(hsi2rgb_class);
  floatinlet_new(&x->x_obj, &x->i_s);
  floatinlet_new(&x->x_obj, &x->i_i);
  x->o_r = outlet_new(&x->x_obj, &s_float);
  x->o_g = outlet_new(&x->x_obj, &s_float);
  x->o_b = outlet_new(&x->x_obj, &s_float);
  return (void*)x;
}

void hsi2rgb_setup(void) {
  hsi2rgb_class = class_new(gensym("hsi2rgb"),
			    (t_newmethod)hsi2rgb_new,
			    (t_method)hsi2rgb_free, sizeof(t_hsi2rgb),
			    CLASS_DEFAULT, 0);
  class_addbang(hsi2rgb_class, hsi2rgb_bang);
  class_addfloat(hsi2rgb_class, hsi2rgb_float);
}
