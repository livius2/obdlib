import elm327
import re


class Response(object):
    """
        This object contains response data and
        includes the common data analyzing
    """
    read_term = '\r\n'

    def __init__(self, data=b'', proto=0):
        # convert to string
        # split by term
        # remove spaces
        buff = re.split('[{}]'.format(self.read_term), data.decode())
        self.raw_data = [line.strip().replace(' ', '') for line in buff if line]
        if proto > 5:
            self.protocol = elm327.ProtoCan(proto)
        else:
            self.protocol = elm327.Proto()

    def _check_value(func):
        """
            Checks response value
            ? - this is a standard response for a misunderstood command
        """

        def wrapper(self):
            if '?' in self.raw_data[:1]:
                return None
            else:
                return func(self)

        return wrapper

    @property
    def value(self):
        """
            Retrieves useful value from data
        """
        return self.protocol.create_data(self.raw_data)

    @property
    @_check_value
    def raw_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data

    @property
    def at_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data[:1][0]