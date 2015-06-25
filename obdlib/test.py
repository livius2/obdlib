import scanner
import time

with scanner.OBDScanner("/dev/pts/7") as scan:
    while True:
        time.sleep(0.5)
        sensor = scan.sensor.RPM
        print "Sensor {}: {} {}".format(sensor.title, sensor.value, sensor.unit)
