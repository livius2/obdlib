from obdlib.obd.pids import *


unit_english = 0


def set_unit(v):
    """
        Sets unit flag
    """
    global unit_english
    unit_english = v


def zfill(string, width):
    """
        Wrapper for str.zfill which is not exists in micropython
        :param string: a string for alignment
        :param width: width of the resulted string
        :return: a string that has been aligned to the width
    """
    return string.zfill(width) \
        if hasattr(string, 'zfill') else ('{0:0%d}' % (width)).format(int(string))


def bitwise_pids(hex_string, start=0):
    """
        Determine supported PIDs based on the supplied hexadecimal string
        :param hex_string:a hex string representing bitwise encoded PID support
        :return: a dictionary of PID number: boolean pairs that indicate
        whether or not a PID is supported
    """
    bits = zfill(bin(int(hex_string, 16))[2:], 32)
    return dict(
        (zfill(hex(i + 1 + start)[2:], 2).upper(), 1 if value == '1' else 0)
        for i, value in enumerate(bits)
    )


def rpm(value):
    """
        Converts the vehicle's current engine RPM value
        :return: the current engine RPM
    """
    return __digit(value) / 4


def speed(value):
    """
        Converts the vehicle's current engine RPM value
        :return: the current engine speed
    """
    value = __digit(value)
    # English - > mph
    if unit_english:
        # km/h - > mph conversion
        value = value * 0.621371192
    return value


def load_value(value):
    """
        Converts the vehicle's current engine load value
        :return: the current engine value
    """
    return __digit(value) * 100 / 255


def term_fuel(value):
    """
        Converts the vehicle's short term fuel or long term fuel
        :return: the current engine value
    """
    return (__digit(value) - 128) * 100 / 128


def fuel_pressure(value):
    """
        Converts the vehicle's fuel pressure
        :return: the current engine value
    """
    value = __digit(value) * 3
    # English - > psi
    if unit_english:
        # kPa - > psi conversion
        value = value * 0.145037738
    return value


def absolute_pressure(value):
    """
        Converts the vehicle's intake manifold absolute pressure
        :return: the current engine value
    """
    value = __digit(value)
    # English - > psi
    if unit_english:
        # kPa - > psi conversion
        value = value * 0.145037738
    return value


def timing_advance(value):
    """
        Converts the vehicle's Timing advance
        :return: the current engine value
    """
    return (__digit(value) - 128) / 2


def air_flow_rate(value):
    """
        Converts the vehicle's MAF air flow rate
        :return: the current engine value
    """
    return __digit(value) / 100


def throttle_pos(value):
    """
        Converts the vehicle's Throttle position
        :return: the current engine value
    """
    return __digit(value) * 100 / 255


def air_status(value):
    """
        Converts the vehicle's Commanded secondary air status
        :return: the current engine value
    """
    return SECONDARY_AIR_STATUS.get(__digit(value), None)


def voltage(value):
    """
        Converts the vehicle's Oxygen sensor voltage
        0 - 1.275 Volts
        :return: the current engine value
    """
    return __digit(value) / 200.0


def coolant_temp(value):
    """
        Converts the vehicle's current engine coolant temperature
        :return: the current engine coolant temperature in degrees Celsius
    """
    # The data returned in the OBD response is in hexadecimal with a zero
    # offset to account for negative temperatures. To return the current
    # temperature in degrees Celsius, we must first convert to decimal and
    # then subtract 40 to account for the zero offset.
    value = __digit(value) - 40
    # English - > F
    if unit_english:
        # C - > F
        value = value * 9 / 5 + 32
    return value


def obd_standards(value):
    """
        Converts the vehicle's OBD standards this vehicle conforms to
        :return: the current engine value
    """
    return OBD_STANDARDS[__digit(value)] if len(OBD_STANDARDS) >= value else None


def time(value):
    """
        Converts the vehicle's Run time since engine start
        :return: the current engine value
    """
    return __digit(value)


def oil_temp(value):
    """
        Converts the vehicle's current engine oil temperature
        :return: the current engine oil temperature in degrees Celsius
    """
    # The data returned in the OBD response is in hexadecimal with a zero
    # offset to account for negative temperatures. To return the current
    # temperature in degrees Celsius, we must first convert to decimal and
    # then subtract 40 to account for the zero offset.
    value = __digit(value) - 40
    # English - > F
    if unit_english:
        # C - > F
        value = value * 9 / 5 + 32
    return value


def ecu_name(value):
    """
        Returns the name of the Engine Control Unit (ECU)
        :return: the name of the ECU (if available)
    """
    return value


def fuel_type(value):
    """
        Converts the vehicle's fuel type
        :return: a description of the type of fuel used by the vehicle
    """
    return FUEL_TYPE_DESCRIPTION.get(__digit(value), None)


def __digit(value):
    """
        Converts hex to digit
    """
    return int(value, 16)
