import elm327
from obd.modes import Modes


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
        # list of pids (available or not)
        self.__pids = {}
        self.__ecus = {}

    def init(self, args):
        """
            Unpacks modes params
            :param args - mode params
        """
        self.title, self.description, self.pid, \
        self.bytes, self.unit, self.__decoder, self.kwargs = args

    @property
    def ecus(self):
        """
            Generates available ECU's value
            :return tuple (ecu, value)
        """
        for ecu, value in self.__ecus.iteritems():
            yield (ecu, value)

    def sensors(self, mode=1):
        """
            Generates available ECU's and PID's value
        """
        for ecu, pids in self.__pids.iteritems():
            for pid, access in pids.iteritems():
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
        if pids and isinstance(pids.__ecus, dict):
            self.__pids.update(pids.__ecus)
            # for ecu in self.__pids.keys():
            #    if self.__pids[ecu][str(20)]:
            #        self.__pids[ecu].update(self[01](int('20', 16)).__ecus[ecu])
            #        if self.__pids[ecu][str(40)]:
            #            self.__pids[ecu].update(self[01](int('40', 16)).__ecus[ecu])
            return True

    def is_pids(self):
        """
            Returns True, if some of the PID's are available
        """
        resp = False
        for ecu, pids in self.__pids.iteritems():
            if True in pids.values():
                resp = True
                break
        return resp

    def _set_value(self, value):
        """
            Converts (if needed) and sets current value of sensor
        """
        if elm327.NO_RESULT != value or value is not None:
            value = self.__decoder(value, **self.kwargs) if self.kwargs else self.__decoder(value)

        return value

    def __getitem__(self, mode):
        try:
            def get_pid(pid):
                self.init(self.__modes.modes[mode][pid])
                self.__ecus.update(
                    dict([k, self._set_value(v)] for k, v in self.__call(self.pid).value.iteritems())
                )
                return self

            return get_pid
        except Exception as err:
            # logging error
            print("Unsupported command.")
