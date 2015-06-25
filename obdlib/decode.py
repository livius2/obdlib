def zfill(string, width):
    """
        Wrapper for str.zfill which is not exists in micropython
        :param string: a string for alignment
        :param width: width of the resulted string
        :return: a string that has been aligned to the width
    """
    return string.zfill(width) \
        if hasattr(string, 'zfill') else ('{0:0%d}' % (width)).format(int(string))


def decode_bitwise_pids(hex_string):
    """
        Determine supported PIDs based on the supplied hexadecimal string
        :param hex_string:a hex string representing bitwise encoded PID support
        :return: a dictionary of PID number: boolean pairs that indicate
        whether or not a PID is supported
    """
    clean_hex = hex_string.replace(' ', '')
    bits = zfill(bin(int(clean_hex, 16))[2:], 32)
    return dict(
        (zfill(hex(i + 1)[2:], 2).upper(), True if value == '1' else False)
        for i, value in enumerate(bits)
    )


def engine_rpm(value):
    """
        Converts the vehicle's current engine RPM value
        :return: the current engine RPM
    """
    return int(value, 16) / 4
