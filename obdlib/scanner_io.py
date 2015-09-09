from obdlib.obd.sensors_io import CommandIO
from obdlib.obdscan import Scanner


class ObdIO(Scanner):
    def __init__(self, *args, **kwargs):
        Scanner.__init__(self, *args, **kwargs)

    def set_sensors(self):
        self.sensor = CommandIO(self.send)
        # checks connection with vehicle
        self.connected = self.sensor.check_pids()
        self.check_connection()
