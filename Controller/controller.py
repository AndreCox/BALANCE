import lcm
import time
import sys
import threading
from simple_pid import PID  # You can use an external PID library or implement your own

sys.path.append('../')
import LCM.wheels_lcm as wheels_lcm
import LCM.imu_lcm as imu_lcm

# Global variable to store IMU data
imu_data = None
lock = threading.Lock()


def imu_handler(channel, data):
    global imu_data
    msg = imu_lcm.imu_t.decode(data)
    with lock:
        imu_data = msg
    print(f"Received IMU data: {msg}")


def control_loop():
    global imu_data

    lc = lcm.LCM()
    lc.subscribe("IMU", imu_handler)

    # PID Controller parameters
    Kp = 1.0  # Proportional gain
    Ki = 0.1  # Integral gain
    Kd = 0.05  # Derivative gain

    pid = PID(Kp, Ki, Kd, setpoint=0.0)  # Setpoint is upright (0 tilt)
    pid.output_limits = (-1.0, 1.0)  # Speed limits for motors

    try:
        while True:
            lc.handle_timeout(10)  # Poll LCM messages

            with lock:
                if imu_data is None:
                    continue
                tilt_error = imu_data.gyro[2]  # Use z-axis gyro as tilt feedback

            # Compute PID output
            correction = pid(tilt_error)

            # Apply correction to wheel speeds
            left_speed = correction
            right_speed = -correction

            publish_speed(lc, left_speed, right_speed)

            time.sleep(0.05)  # Control loop interval
    except KeyboardInterrupt:
        print("Balancing interrupted.")
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
    control_loop()
