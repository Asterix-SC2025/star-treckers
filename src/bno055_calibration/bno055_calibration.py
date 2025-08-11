import time
import json
import board
import busio
import adafruit_bno055

CAL_FILE = "bno055_calibration.json"

def run_calibration():
    """Run BNO055 calibration process."""
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    def save_calibration():
        cal_data = {
            "accel_offset": sensor.offsets_accelerometer,
            "gyro_offset": sensor.offsets_gyroscope,
            "mag_offset": sensor.offsets_magnetometer,
            "accel_radius": sensor.radius_accelerometer,
            "mag_radius": sensor.radius_magnetometer
        }
        with open(CAL_FILE, "w") as f:
            json.dump(cal_data, f)
        print("Calibration saved to", CAL_FILE)

    def load_calibration():
        with open(CAL_FILE, "r") as f:
            cal_data = json.load(f)
        sensor.offsets_accelerometer = tuple(cal_data["accel_offset"])
        sensor.offsets_gyroscope = tuple(cal_data["gyro_offset"])
        sensor.offsets_magnetometer = tuple(cal_data["mag_offset"])
        sensor.radius_accelerometer = cal_data["accel_radius"]
        sensor.radius_magnetometer = cal_data["mag_radius"]
        print("Calibration loaded from", CAL_FILE)

    try:
        load_calibration()
        print("Using stored calibration. No need to spin the sensor!")
    except FileNotFoundError:
        print("No calibration file found. Please rotate the sensor to calibrate...")
        while True:
            cal_status = sensor.calibration_status
            print("Calibration status:", cal_status)
            if all(x == 3 for x in cal_status):
                print("Fully calibrated!")
                save_calibration()
                break
            time.sleep(1)

    while True:
        print("Heading, Roll, Pitch:", sensor.euler)
        time.sleep(0.5)
