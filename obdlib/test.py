import scanner
import time


# Retrieves all available sensor values
with scanner.OBDScanner("/dev/pts/5") as scan:
    while True:
        data = {}
        for sensor in scan.sensor.sensors(mode=01):
            # gets available sensor value only
            data[sensor.title] = sensor.value
        print("---------------------------------------")
        print(data)
        time.sleep(0.5)

# Retrieves value from one sensor
with scanner.OBDScanner("/dev/pts/5") as scan:
    while True:
        # Engine coolant temperature
        sensor = scan.sensor[01](05)
        print("Sensor {}: {} {}".format(sensor.title, sensor.value, sensor.unit))
        time.sleep(0.5)