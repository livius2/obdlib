from glob import glob
import serial

PORTS = (
    "/dev/rfcomm[0-9]*",  # Bluetooth ports
    "/dev/ttyUSB[0-9]*",  # USB ports
    "/dev/pts/[0-9]*"  # OBDSim ports
)


def check_port(port):
    """try to open port. Returns True or False result"""
    result = False
    try:
        ser = serial.Serial(port)
        ser.close()
        result = True
    except:
        pass

    return result


def serial_scan():
    """scan for available ports. return a list of serial names"""
    available = []
    ports = []
    for possible in PORTS:
        ports += glob(possible)

    for port in ports:
        if check_port(port):
            available.append(port)

    return available
