class Response(object):
    """
        This object contains response data and
        includes the common data analyzing
    """
    read_term = '\r\n'

    def __init__(self, data):
        # convert to string
        # split by term
        # remove spaces
        buff = data.decode().split(self.read_term)
        self.raw_data = [line.strip().replace(' ', '') for line in buff if line]

    @property
    def value(self):
        """
            Retrieves useful value from data
        """
        value = None
        r_value = self.raw_data[0]
        if r_value:
            if len(r_value) >= 6 and len(r_value) <= 12:
                # remove first 4 characters. This are service bytes from ELM
                # ! 4 characters if headers are disabled
                #         [ value ]
                # ex: 4100FFFFFFFF
                value = r_value[4:]
            else:
                # logging error
                print("Dropped bytes! The frame size is not suitable.")

        return value


    @property
    def raw_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data
