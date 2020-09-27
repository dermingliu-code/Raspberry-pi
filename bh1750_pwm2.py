#!/usr/bin/python
#---------------------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bh1750.py
# Read data from a BH1750 digital light sensor.
#
# Author : Matt Hawkins
# Date   : 26/06/2018
#
# For more information please visit :
# https://www.raspberrypi-spy.co.uk/?s=bh1750
#
#---------------------------------------------------------------------
import smbus
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
time.sleep(1)
def led_pwm():
	LED_PIN = [23,24]
	PWM_FREQ = 50
	GPIO.setmode(GPIO.BCM)
	for i in LED_PIN:
		GPIO.setup(i, GPIO.OUT)
		GPIO.output(i,0)
	pwm1 = GPIO.PWM(23, PWM_FREQ)
        pwm2 = GPIO.PWM(24, PWM_FREQ)
	pwm1.start(0)
        pwm2.start(100)
       	for duty_cycle in range(0, 100, 5):
            pwm1.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeDutyCycle(100-duty_cycle)
            time.sleep(0.05)
        for duty_cycle in range(100, 0, -5):
       	    pwm1.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeDutyCycle(100-duty_cycle)
            time.sleep(0.05)
def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  time.sleep(0.1)
  return convertToNumber(data)

try:
  while True:
    lightLevel=readLight()
    print("Light Level : " + format(lightLevel,'.2f') + " lx")
    if lightLevel <= 30:
	led_pwm()
    else:
	pass
    time.sleep(10)
except KeyboardInterrupt:
	GPIO.cleanup()
