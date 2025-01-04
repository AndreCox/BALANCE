import lcm
import bmx160 as imu
import sys
import time
sys.path.append('../')

import LCM.imu_lcm as imu_lcm

lc = lcm.LCM()
bmx160 = imu.BMX160(1)

while True:
    try:
        print("Initializing BMX160...")
        bmx160.begin()
        break
    except:
        print("BMX160 not found or there was an error initializing the sensor. Retrying...")
        time.sleep(1)
        pass

print("Starting LCM IMU routine")
while True:
    all_sensor_data = bmx160.get_all_data()
    mag = all_sensor_data[0:3]
    gyro = all_sensor_data[3:6]
    accl = all_sensor_data[6:9]

    try:
        msg = imu_lcm.imu_t()
        msg.mag = mag
        msg.gyro = gyro
        msg.accl = accl

        lc.publish("IMU", msg.encode())
    except Exception as e:
        print(f"Error publishing data: {e}")
