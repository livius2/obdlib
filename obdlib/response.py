class Response(object):
    """
        This object contains response data and
        includes the common data analyzing
    """

    __slots__ = ['raw_data', 'protocol', 'proto_num']

    def __init__(self, data=b'', proto_num=0):
        # convert to string
        # split by term
        # remove spaces
        buff = data.decode().replace('\n', '').split('\r')
        self.raw_data = [line.strip().replace(' ', '')
                         for line in buff if line]
        self.protocol = None
        self.proto_num = proto_num

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
            :return dictionary: key - ECU, value - frame data
        """
        # init protocol (CAN or rest)
        if self.protocol is None:
            from obdlib.obd.protocols import protocols, can_protocols

            self.protocol = can_protocols.ProtocolsCan(
                self.proto_num) if self.proto_num > 5 else protocols.Protocols()

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
        return self.raw_data[:1][0] if self.raw_data else []
