import elm327
import re


class Response(object):
    """
        This object contains response data and
        includes the common data analyzing
    """
    read_term = '\r\n'

    def __init__(self, data=b''):
        # convert to string
        # split by term
        # remove spaces
        print(data)
        buff = re.split('[{}]'.format(self.read_term), data.decode())
        self.raw_data = [line.strip().replace(' ', '') for line in buff if line]
        print(self.raw_data)

    @property
    def value(self):
        """
            Retrieves useful value from data
        """
        r_value = self.raw_data[0] if self.raw_data else None
        if r_value:
            if len(r_value) >= 4 and len(r_value) <= 16:
                # remove first 4 characters. This are service bytes from ELM
                # ! 4 characters if headers are disabled
                #         [ value ]
                # ex: 4100FFFFFFFF
                r_value = r_value if r_value == elm327.NO_RESULT else r_value[4:]
            else:
                # logging error
                print("Dropped bytes! The frame size is not suitable.")

        return r_value


    @property
    def raw_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data
