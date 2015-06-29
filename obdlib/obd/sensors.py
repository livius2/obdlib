import elm327
from modes import Modes


class Command(object):
    """
        This class to provide the common functionality
        to make PID's request
    """

    def __init__(self, call_obd, units):
        """
            Init the common params
            :param call_obd: request function
            :param units: flag of conversion (0 - Europe, 1 - English, ex: km/h - > mph)
        """
        self.__modes = Modes(units)
        self.__call = call_obd
        self.__decoder = lambda: None
        self.title = None
        self.description = None
        self.pid = None
        self.bytes = None
        self.value = None
        self.unit = None
        self.kwargs = None
        self.__sensors = {}
        # list of pids (available or not)
        self.__pids = {}

    def init(self, args):
        self.title, self.description, self.pid, \
        self.bytes, self.unit, self.__decoder, self.kwargs = args

    def sensors(self, mode):
        for pid, access in self.__pids.iteritems():
            pid = int(pid, 16)
            if not access or pid in (0, 32, 64,):
                continue
            self[mode](pid)
            yield self

    def check_pids(self):
        """
            Checks available PIDs. If return data, it means connected True
            Prepares the ELM327 for communicating with vehicle - 01 pid 00
        """
        pids = self[01](00)
        if pids:
            if isinstance(pids.value, dict):
                self.__pids.update(pids.value)
                # if self.__pids[20]:
                # self.__pids.update(self[01](20).value)
                # if self.__pids[40]:
                # self.__pids.update(self[01](40).value)
                return True

    def is_pids(self):
        """
            Returns True, if some of the PID's are available
        """
        return True in self.__pids.values()

    def _set_value(self, value):
        """
            Converts (if needed) and sets current value of sensor
        """
        if elm327.NO_RESULT == value or value is None:
            self.value = value
        else:
            self.value = self.__decoder(value, **self.kwargs) if self.kwargs else self.__decoder(value)

    def __getitem__(self, mode):
        try:
            def get_pid(pid):
                self.init(self.__modes.modes[mode][pid])
                self._set_value(
                    self.__call(self.pid).value
                )
                return self

            return get_pid
        except Exception as err:
            # logging error
            raise Exception("Unsupported command.")
