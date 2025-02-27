#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://raspberrytips.nl/tm1637-4-digit-led-display-raspberry-pi/
import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637
#CLK -> GPIO23 (Pin 5)
#DI0 -> GPIO24 (Pin 25)
GPIO.setmode(GPIO.BCM)
Display = tm1637.TM1637(5,25,tm1637.BRIGHT_TYPICAL)

Display.Clear()
Display.SetBrightnes(2)  # from 0 to 7
try:
 while(True):
   now = datetime.datetime.now()
   hour = now.hour
   minute = now.minute
   second = now.second
   currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ]
   Display.Show(currenttime)
   Display.ShowDoublepoint(second % 2)
   time.sleep(1)
except KeyboardInterrupt:
	Display.Clear()
