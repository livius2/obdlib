import scanner
import time


# Retrieves value from one sensor
with scanner.OBDScanner("/dev/pts/6") as scan:
    while True:
        if scan.sensor:
            if scan.sensor.is_pids():
                # Engine coolant temperature
                sensor = scan.sensor[01](05)
                print("Sensor {}: {} {}".format(sensor.title, sensor.value, sensor.unit))
                time.sleep(0.5)
            else:
                raise Exception("Pids are not supported")
        else:
            break

# Retrieves all available sensor values
with scanner.OBDScanner("/dev/pts/6") as scan:
    while True:
        if scan.sensor and scan.sensor.is_pids():
            data = {}
            for sensor in scan.sensor.sensors(mode=1):
                # gets available sensor value only
                data[sensor.title] = sensor.value
            print("---------------------------------------")
            print(data)
            time.sleep(0.5)
        else:
            break



