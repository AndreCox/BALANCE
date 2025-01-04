import lcm
import time
import sys

sys.path.append('../')
import LCM.wheels_lcm as wheels_lcm

def ramp_speed():
    lc = lcm.LCM()

    # Ramp parameters
    ramp_duration = 10.0  # Time to ramp from -1 to 1 in seconds
    step_interval = 0.05  # Time between steps in seconds

    # Calculate the step size for each interval
    steps = int(ramp_duration / step_interval)
    speed_step = 2.0 / steps  # Covers the range -1 to 1

    try:
        while True:
            # Ramp up from -1 to 1
            for i in range(steps + 1):
                speed = -1.0 + i * speed_step
                publish_speed(lc, speed, speed)
                time.sleep(step_interval)

            # Ramp down from 1 to -1
            for i in range(steps + 1):
                speed = 1.0 - i * speed_step
                publish_speed(lc, speed, speed)
                time.sleep(step_interval)
    except KeyboardInterrupt:
        print("Ramp test interrupted.")
    finally:
        # Stop the motors
        publish_speed(lc, 0.0, 0.0)


def publish_speed(lc, speed_l, speed_r):
    # Create and populate the LCM message
    msg = wheels_lcm.wheels_t()
    msg.speed_l = speed_l
    msg.speed_r = speed_r

    # Publish the message
    print(f"Publishing speed: Left = {speed_l}, Right = {speed_r}")
    lc.publish("WHEELS", msg.encode())

if __name__ == "__main__":
    ramp_speed()
