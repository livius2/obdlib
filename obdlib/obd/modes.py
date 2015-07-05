from obdlib.utils import *

# OBD Modes (described in OBD-II standard SAE J1979)
CURRENT_DATA = 1
FREEZE_FRAME_DATA = "02"
REQUEST_TROUBLE_CODES = "03"
CLEAR_TROUBLE_CODES_AND_VALUES = "04"
OXYGEN_SENSOR_DATA = "05"
SYSTEM_MONITORING_DATA = "06"
PENDING_TROUBLE_CODES = "07"
CONTROL_OPERATION = "08"
VEHICLE_INFORMATION_DATA = "09"
PERMANENT_TROUBLE_CODES = "0A"

DEFAULT_OBD_MODE = CURRENT_DATA


class Modes(object):
    """
        Provides list of OBD modes
    """
    __slots__ = ['modes']

    def __init__(self, units):
        set_unit(units)
        # In order to choose right pid you
        # need to do next request (ex: get engine coolant temperature - self.modes[01][05])
        self.modes = {
            # Show current data - 01
            CURRENT_DATA: (
                (
                    "PIDS_01-20",  # pid title
                    "PIDs supported [01 - 20]",  # pid description
                    "0100",  # command
                    4,  # Data bytes returned
                    "",  # Units
                    bitwise_pids,  # Callback
                    {"start": 0}  # Additional params, must be dict
                ),
                ("DTC_STATUS", "Monitor status since DTCs cleared", "0101", 4, "", lambda v: v, None),
                ("FREEZE", "Freeze DTC", "0102", 2, "", lambda v: v, None),
                ("FUEL_ST", "Fuel system status", "0103", 2, "", lambda v: v, None),
                ("ENGINE_LV", "Calculated engine load value", "0104", 1, "%", load_value, None),
                ("COOLANT_TEMP", "Engine coolant temperature", "0105", 1, "C", coolant_temp, None),
                ("STF1", "Short term fuel % trim_Bank 1", "0106", 1, "%", term_fuel, None),
                ("LTF1", "Long term fuel % trim_Bank 1", "0107", 1, "%", term_fuel, None),
                ("STF2", "Short term fuel % trim_Bank 2", "0108", 1, "%", term_fuel, None),
                ("LTF2", "Long term fuel % trim_Bank 2", "0109", 1, "%", term_fuel, None),
                ("FUEL_PR", "Fuel pressure", "010A", 1, "kPa", fuel_pressure, None),
                ("IMAP", "Intake manifold absolute pressure", "010B", 1, "kPa", absolute_pressure, None),
                ("RPM", "Engine RPM", "010C", 2, "rpm", rpm, None),
                ("SPEED", "Vehicle speed", "010D", 1, "km/h", speed, None),
                ("ADV_TIMING", "Timing advance", "010E", 1, "degrees", timing_advance, None),
                ("AIR_TEMP", "Intake air temperature", "010F", 1, "C", coolant_temp, None),
                ("MAF", "MAF air flow rate", "0110", 2, "grams/sec", air_flow_rate, None),
                ("TP", "Throttle position", "0111", 1, "%", throttle_pos, None),
                ("AIR_ST", "Commanded secondary air status", "0112", 1, "", air_status, None),
                ("OS_A", "Oxygen sensors present", "0113", 1, "", lambda v: v, None),
                ("OS11", "Bank 1, Sensor 1 - voltage", "0114", 2, "Volts", voltage, None),
                ("OS12", "Bank 1, Sensor 2 - voltage", "0115", 2, "Volts", voltage, None),
                ("OS13", "Bank 1, Sensor 3 - voltage", "0116", 2, "Volts", voltage, None),
                ("OS14", "Bank 1, Sensor 4 - voltage", "0117", 2, "Volts", voltage, None),
                ("OS21", "Bank 2, Sensor 1 - voltage", "0118", 2, "Volts", voltage, None),
                ("OS22", "Bank 2, Sensor 2 - voltage", "0119", 2, "Volts", voltage, None),
                ("OS23", "Bank 2, Sensor 3 - voltage", "011A", 2, "Volts", voltage, None),
                ("OS24", "Bank 2, Sensor 4 - voltage", "011B", 2, "Volts", voltage, None),
                ("OBD", "OBD standards this vehicle conforms to", "011C", 1, "", obd_standards, None),
                ("OS_B", "Oxygen sensors present", "011D", 1, "", lambda v: v, None),
                ("AIS", "Auxiliary input status", "011E", 1, "", lambda v: v, None),
                ("ENGINE_TIME", "Run time since engine start", "011F", 2, "seconds", time, None),

                ("PIDS_20-40", "PIDs supported [20 - 40]", "0120", 4, "", bitwise_pids, {"start": 32}),
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

                ("PIDS_C", "PIDs supported [40 - 60]", "0140", 4, "", bitwise_pids, {"start": 64}),
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
        }
