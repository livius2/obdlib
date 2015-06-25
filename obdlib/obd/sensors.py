from decode import *

# Show current data
MODE_1 = {
    "PIDS_A": ("PIDs supported [01 - 20]", "01", "00", 4, "", decode_bitwise_pids),
    "DTC_STATUS": ("Monitor status since DTCs cleared", "01", "01", 4, "", lambda: None),
    "FREEZE": ("Freeze DTC", "01", "02", 2, "", lambda: None),
    "RPM": ("Engine RPM", "01", "0C", 2, "rpm", engine_rpm),
}


class Command(object):
    def __init__(self, call_obd=None):
        self.__modes = MODE_1
        self.__call = call_obd
        self.__decoder = lambda: None
        self.description = None
        self.mode = None
        self.pid = None
        self.bytes = None
        self.unit = None
        self.title = None
        self.value = None

    def init(self, cmd, args):
        self.title = cmd
        self.description, self.mode, self.pid, self.bytes, self.unit, self.__decoder = args

    def _get_cmd(self):
        return self.mode + self.pid

    def _set_value(self, value):
        self.value = self.__decoder(value)

    def __getattr__(self, item):
        try:
            self.init(item, self.__modes[item])
            self._set_value(
                self.__call(self._get_cmd()).value
            )

            return self
        except Exception as err:
            # logging error
            print err
