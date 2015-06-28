from decode import *
import elm327

MODES = (
    (),
        # Show current data MODE_1
        (
            ("PIDS_A", "PIDs supported [01 - 20]", "01", "00", 4, "", decode_bitwise_pids, {"start": 0}),
            ("DTC_STATUS", "Monitor status since DTCs cleared", "01", "01", 4, "", lambda v: v, None),
            ("FREEZE", "Freeze DTC", "01", "02", 2, "", lambda v: v, None),
            ("FUEL_ST", "Fuel system status", "01", "03", 2, "", lambda v: v, None),
            ("ENGINE_LV", "Calculated engine load value", "01", "04", 1, "%", engine_load_value, None),
            ("COOLANT_TEMP", "Engine coolant temperature", "01", "05", 1, "C", engine_coolant_temp, None),
            ("STF1", "Short term fuel % trim_Bank 1", "01", "06", 1, "%", term_fuel, None),
            ("LTF1", "Long term fuel % trim_Bank 1", "01", "07", 1, "%", term_fuel, None),
            ("STF2", "Short term fuel % trim_Bank 2", "01", "08", 1, "%", term_fuel, None),
            ("LTF2", "Long term fuel % trim_Bank 2", "01", "09", 1, "%", term_fuel, None),
            ("FUEL_PR", "Fuel pressure", "01", "0A", 1, "kPa", fuel_pressure, None),
            ("IMAP", "Intake manifold absolute pressure", "01", "0B", 1, "kPa", absolute_pressure, None),
            ("RPM", "Engine RPM", "01", "0C", 2, "rpm", engine_rpm, None),
            ("SPEED", "Vehicle speed", "01", "0D", 1, "km/h", engine_speed, None),
            ("ADV_TIMING", "Timing advance", "01", "0E", 1, "degrees", timing_advance, None),
            ("AIR_TEMP", "Intake air temperature", "01", "0F", 1, "C", engine_coolant_temp, None),
            ("MAF", "MAF air flow rate", "01", "10", 2, "grams/sec", air_flow_rate, None),
            ("TP", "Throttle position", "01", "11", 1, "%", throttle_pos, None),
            ("AIR_ST", "Commanded secondary air status", "01", "12", 1, "", air_status, None),
            ("OS_A", "Oxygen sensors present", "01", "13", 1, "", lambda v: v, None),
            ("OS11", "Bank 1, Sensor 1 - voltage", "01", "14", 2, "Volts", sensor_voltage, None),
            ("OS12", "Bank 1, Sensor 2 - voltage", "01", "15", 2, "Volts", sensor_voltage, None),
            ("OS13", "Bank 1, Sensor 3 - voltage", "01", "16", 2, "Volts", sensor_voltage, None),
            ("OS14", "Bank 1, Sensor 4 - voltage", "01", "17", 2, "Volts", sensor_voltage, None),
            ("OS21", "Bank 2, Sensor 1 - voltage", "01", "18", 2, "Volts", sensor_voltage, None),
            ("OS22", "Bank 2, Sensor 2 - voltage", "01", "19", 2, "Volts", sensor_voltage, None),
            ("OS23", "Bank 2, Sensor 3 - voltage", "01", "1A", 2, "Volts", sensor_voltage, None),
            ("OS24", "Bank 2, Sensor 4 - voltage", "01", "1B", 2, "Volts", sensor_voltage, None),
            ("OBD", "OBD standards this vehicle conforms to", "01", "1C", 1, "", obd_standards, None),
            ("OS_B", "Oxygen sensors present", "01", "1D", 1, "", lambda v: v, None),
            ("AIS", "Auxiliary input status", "01", "1E", 1, "", lambda v: v, None),
            ("ENGINE_TIME", "Run time since engine start", "01", "1F", 2, "seconds", engine_time, None),

            ("PIDS_B", "PIDs supported [20 - 40]", "01", "20", 4, "", decode_bitwise_pids, {"start": 32}),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),

            ("PIDS_C", "PIDs supported [40 - 60]", "01", "40", 4, "", decode_bitwise_pids, {"start": 64}),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
            (),
        )
)


class Command(object):
    def __init__(self, call_obd, units):
        self.__call = call_obd
        self.__decoder = lambda: None
        self.title = None
        self.description = None
        self.mode = None
        self.pid = None
        self.bytes = None
        self.value = None
        self.unit = None
        self.kwargs = None
        self.__sensors = {}
        # list of pids (available or not)
        self.__pids = {}
        set_unit(units)

    def init(self, args):
        self.title, self.description, self.mode, self.pid, \
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
                # self.__pids.update(self[01](20).value)
                # self.__pids.update(self[01](40).value)
                return True

    def _get_cmd(self):
        return self.mode + self.pid

    def _set_value(self, value):
        if elm327.NO_RESULT == value or value is None:
            self.value = value
        else:
            self.value = self.__decoder(value, **self.kwargs) if self.kwargs else self.__decoder(value)

    def __getitem__(self, mode):
        try:
            def args_wrapper(pid):
                self.init(MODES[mode][pid])
                self._set_value(
                    self.__call(self._get_cmd()).value
                )
                return self

            return args_wrapper
        except Exception as err:
            # logging error
            raise Exception("Unsupported command.")

    def __getattr__(self, item):
        try:
            self.init(item, self.__modes[item])
            self._set_value(
                self.__call(self._get_cmd()).value
            )

            return self
        except Exception as err:
            # logging error
            raise Exception("Unsupported command.")
