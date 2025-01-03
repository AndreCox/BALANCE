import lcm
import sys
import time
import RPi.GPIO as GPIO
sys.path.append('../')

import LCM.wheels_lcm as wheels_lcm

lc = lcm.LCM()

int_r = [26, 19]
int_l = [20, 21]

GPIO.setmode(GPIO.BOARD)

# set up the GPIO pins as outputs for the motors DRV8871 driver
GPIO.setup(int_r, GPIO.OUT)
GPIO.setup(int_l, GPIO.OUT)

# Now just to test make a loop that turns the motors on and off 
# back and forth

for i in range(10):
    GPIO.output(int_r[0], GPIO.HIGH)
    GPIO.output(int_l[0], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(int_r[0], GPIO.LOW)
    GPIO.output(int_l[0], GPIO.LOW)
    time.sleep(1)
    GPIO.output(int_r[1], GPIO.HIGH)
    GPIO.output(int_l[1], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(int_r[1], GPIO.LOW)
    GPIO.output(int_l[1], GPIO.LOW)