import lcm
import sys
import time
import RPi.GPIO as GPIO
sys.path.append('../')

import LCM.wheels_lcm as wheels_lcm

# LCM Setup
lc = lcm.LCM()

# Motor control GPIO pins
int_r = [26, 19]  # Right motor control pins
int_l = [20, 21]  # Left motor control pins

# Setup GPIO for BCM mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for motor control
GPIO.setup(int_r, GPIO.OUT)
GPIO.setup(int_l, GPIO.OUT)

# Set up PWM on the motor pins with 100Hz frequency (you can adjust this)
pwm_r = [GPIO.PWM(int_r[0], 100), GPIO.PWM(int_r[1], 100)]
pwm_l = [GPIO.PWM(int_l[0], 100), GPIO.PWM(int_l[1], 100)]

# Start PWM with 0% duty cycle (motors off)
pwm_r[0].start(0)
pwm_r[1].start(0)
pwm_l[0].start(0)
pwm_l[1].start(0)

def wheels_handler(channel, data):
    msg = wheels_lcm.wheels_t.decode(data)
    
    # Calculate PWM duty cycle based on speed values
    speed_l = msg.speed_l
    speed_r = msg.speed_r

    # Ensure values are within -1 to 1 range
    speed_l = max(min(speed_l, 1), -1)
    speed_r = max(min(speed_r, 1), -1)

    # Convert the -1 to 1 speed into 0 to 100 PWM duty cycle
    pwm_left_duty = (speed_l + 1) * 50  # Mapping [-1, 1] to [0, 100]
    pwm_right_duty = (speed_r + 1) * 50  # Mapping [-1, 1] to [0, 100]

    # Set PWM for left and right motors
    if speed_l >= 0:
        pwm_l[0].ChangeDutyCycle(pwm_left_duty)
        pwm_l[1].ChangeDutyCycle(0)
    else:
        pwm_l[0].ChangeDutyCycle(0)
        pwm_l[1].ChangeDutyCycle(pwm_left_duty)

    if speed_r >= 0:
        pwm_r[0].ChangeDutyCycle(pwm_right_duty)
        pwm_r[1].ChangeDutyCycle(0)
    else:
        pwm_r[0].ChangeDutyCycle(0)
        pwm_r[1].ChangeDutyCycle(pwm_right_duty)

# Subscribe to the LCM channel for wheels control
lc.subscribe("WHEELS", wheels_handler)

# Main loop to process incoming messages without sleep
try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass
finally:
    # Clean up PWM and GPIO settings on exit
    pwm_r[0].stop()
    pwm_r[1].stop()
    pwm_l[0].stop()
    pwm_l[1].stop()
    GPIO.cleanup()
