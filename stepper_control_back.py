#!/usr/bin/python3
import stepper         # stepper motor class
import PCF8591         # PCF8591 class (ADC)
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


i2c_address = 0x80        # change to your real ADC address
p1,p2,p3,p4 = 18,23,24,25 # stepper motor pins
led = 14

adc = PCF8591(i2c_address)    # instantiate the ADC
motor = stepper(p1,p2,p3,p4)  # instantiate the stepper with given GPIO pins

try:
  while True:
    with open("stepper_control.txt", 'r') as f:
      data = json.load(f)
      angle = int(data['angle'])
      speed = int(data['speed'])
    if angle == -1:     # user has asked to zero the motor
      # Turn on the LED (we could have built this into the
      # zero() method, but keeping it separate make zero() more
      # flexible and less cumbersome):
      GPIO.output(led, 1)
      stepper.zero()       # zero the motor
      GPIO.output(led, 0)  # turn LED off
      # need to write the new zero angle to the file to
      # prevent the zero method from being repeatedly executed:
      with open("stepper_control.txt", 'w') as f:
        data = {"angle":0, "speed":speed} 
        json.dump(data,f)
     else:              # change the motor to the user-defined angle
      stepper.goAngle(angle,float(speed)/100.0)
    time.sleep(0.1)    # small sleep step to avoid re-opening the file too often
except KeyboardInterrupt:
  GPIO.clear()