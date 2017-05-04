#!/usr/bin/env python

import picamera
#from fractions import Fraction
import time
import datetime

def webcam():
	cam = picamera.PiCamera()
	cam.resolution = (800, 600)
	#cam.framerate = Fraction(1, 6)
	#cam.iso = 800
	cam.annotate_text_size = 12
	cam.vflip = False 
	cam.awb_mode = 'auto'
	cam.exposure_mode = 'auto'
	cam.drc_strength = 'high'

	time.sleep(2)

	while True:
	    dt = datetime.datetime.now()
	    cam.annotate_text = dt.strftime('%Y-%m-%d  %H:%M')
	    cam.capture('/home/pi/webcam/webcam.jpg', quality=10)

	    print "Capture at {}".format(dt)

	    time.sleep(60)


if __name__ == "__main__":
	webcam()
