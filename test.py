#!/usr/bin/env python

import random, math
from figen import ImageGenerator


@ImageGenerator(600, 600)
def test(x, y) :
	val = int(((x + y) / 1200.0) * 255)
	return 0, val / 2, val

"""
char red_fn(int i,int j){
    float x=0,y=0,k=0,X,Y;while(k++<256e2&&(X=x*x)+(Y=y*y)<4)y=2*x*y+(j-89500)/102400.,x=X-Y+(i-14680)/102400.;return log(k)/10.15*256;
}
char green_fn(int i,int j){
    float x=0,y=0,k=0,X,Y;while(k++<256e2&&(X=x*x)+(Y=y*y)<4)y=2*x*y+(j-89500)/102400.,x=X-Y+(i-14680)/102400.;return log(k)/10.15*256;
}
char blue_fn(int i,int j){
    float x=0,y=0,k=0,X,Y;while(k++<256e2&&(X=x*x)+(Y=y*y)<4)y=2*x*y+(j-89500)/102400.,x=X-Y+(i-14680)/102400.;return 128-k/200;
}
"""

@ImageGenerator(1024, 1024)
def simplemandelbrot(x, y) :
	a = b = n = 0
	while n+1 < 256e2 and a*a + b*b < 4 :
		n += 1
		A = a*a
		B = b*b
		b = 2 * a * b + (y - 89500) / 102400.0
		a = A - B + (x - 14680) / 102400.0
	r = g = int(math.log(n) / 10.15 * 256)
	b = int(128 - n / 200.0)
	return r, g, b

"""
unsigned char RD(int i,int j){
   double a=0,b=0,c,d,n=0;
   while((c=a*a)+(d=b*b)<4&&n++<880)
   {b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
   return 255*pow((n-80)/800,3.);
}
unsigned char GR(int i,int j){
   double a=0,b=0,c,d,n=0;
   while((c=a*a)+(d=b*b)<4&&n++<880)
   {b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
   return 255*pow((n-80)/800,.7);
}
unsigned char BL(int i,int j){
   double a=0,b=0,c,d,n=0;
   while((c=a*a)+(d=b*b)<4&&n++<880)
   {b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
   return 255*pow((n-80)/800,.5);
}
"""

@ImageGenerator(1024, 1024)
def mandelbrot(x, y) :
	def inner() :
		a = b = 0
		for n in range(1, 880) :
			if a*a + b*b >= 4 :
				c, d = a*a, b*b
				b = (y * 8e-9 - 0.645411) + 2 * a * b
				a = (x * 8e-9 + 0.356888) + c - d
			else :
				return n

	val = inner()
	return [ int(abs((255 * ((val - 80) / 800.0 + 0j)**i).real)) for i in (3, .7, .5) ]

def main() :
	simplemandelbrot.generate().show()

if __name__ == "__main__" :
	main()
