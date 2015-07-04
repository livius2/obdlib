import scanner
import time

# Example 1
# Retrieves value from one sensor
with scanner.OBDScanner("/dev/pts/5") as scan:
    while True:
        if scan.sensor:
            if scan.sensor.is_pids():
                # Engine coolant temperature
                sensor = scan.sensor[01](05)
                # two or more ECU's respond to one request
                # we should be prepared for it
                for ecu, value in sensor.ecus:
                    print("ECU: {} Sensor {}: {} {}".format(ecu, sensor.title, value, sensor.unit))
                time.sleep(0.5)
            else:
                raise Exception("Pids are not supported")
        else:
            break

# Example 2
# Retrieves all available sensor values
with scanner.OBDScanner("/dev/pts/5") as scan:
    while True:
        if scan.sensor:
            if scan.sensor.is_pids():
                data = {}
                # gets available sensor value only
                for sensor in scan.sensor.sensors():
                    # two or more ECU's respond to one request
                    # we should be prepared for it
                    ecus_value = {}
                    for ecu, value in sensor.ecus:
                        ecus_value[ecu] = value
                    data[sensor.title] = ecus_value
                print("---------------------------------------")
                print(data)
                time.sleep(0.5)
            else:
                raise Exception("Pids are not supported")
        else:
            break