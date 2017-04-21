#!/usr/bin/env python

import picamera
#from fractions import Fraction
import time
import datetime

cam = picamera.PiCamera()
cam.resolution = (800, 600)
#cam.framerate = Fraction(1, 6)
#cam.iso = 800
cam.annotate_text_size = 12

time.sleep(2)

while True:
    dt = datetime.datetime.now()
    cam.annotate_text = dt.strftime('%Y-%m-%d  %H:%M')
    cam.capture('/home/pi/webcam/webcam.jpg')

    print "Capture at {}".format(dt)

    time.sleep(60)

