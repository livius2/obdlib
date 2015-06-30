import re

# AT command strings
RESET_COMMAND = "ATZ"
ECHO_OFF_COMMAND = "ATE0"
HEADER_ON_COMMAND = "ATH1"
SPACES_OFF_COMMAND = "ATS0"
LINEFEED_OFF_COMMAND = "ATL0"
BATTERY_VOLTAGE_COMMAND = "ATRV"
MEMORY_OFF_COMMAND = "ATM0"

SET_PROTOCOL_AUTO_COMMAND = "ATSPA8"
DESCRIBE_PROTOCOL_COMMAND = "ATDP"
DESCRIBE_PROTOCOL_NUMBER_COMMAND = "ATDPN"

DEFAULT_RETRIES = 10
NO_RESULT = "NODATA"


class Elm327(object):
    pass


class Protocols(object):
    def __init__(self):
        self.protocols = {
            0: ('Automatic',),
            1: ('SAE J1850 PWM (41.6 kbaud)',),
            2: ('SAE J1850 VPW (10.4 kbaud)',),
            3: ('ISO 9141-2  (5 baud init, 10.4 kbaud)',),
            4: ('ISO 14230-4 KWP (5 baud init, 10.4 kbaud)',),
            5: ('ISO 14230-4 KWP (fast init, 10.4 kbaud)',),
            6: ('ISO 15765-4 CAN (bit:11, baud:500)', 11, 500),
            7: ('ISO 15765-4 CAN (bit:29, baud:500)', 29, 500),
            8: ('ISO 15765-4 CAN (bit:11, baud:250)', 11, 250),
            9: ('ISO 15765-4 CAN (bit:29, baud:250)', 29, 250),
            'A': ('SAE J1939 CAN (bit:29, baud:250)', 29, 250),
            'B': 'USER1 CAN (11* bit ID, 125* kbaud)',
            'C': 'USER2 CAN (11* bit ID, 50* kbaud)',
        }

    def create_data(self, data):
        raise NotImplementedError()

    @classmethod
    def remove_searching(cls, data):
        """
            Removes SEARCHING... string
            This appears after OBD command 01 00 (checks available PID's)
        """
        try:
            pos = data.index('SEARCHING...')
            if pos != 1:
                data.pop(pos)
        except ValueError:
            pass

        return data

    @classmethod
    def check_result(cls, data):
        """
            Checks the data. Return False, if the data equal 'NO DATA'
        """
        return False if data == NO_RESULT else True

    @classmethod
    def check_error(cls, data):
        """
            Checks the error data. The data starts with 7F
            format: 7F mode code
        """
        response = True
        codes = {
            10: 'general reject',
            11: 'service not supported',
            12: 'invalid format',
            21: 'busy',
            22: 'conditions not correct',
            78: 'pending replies'
        }
        if data[0][0:2] == '7F':
            # logging error
            print('Error: mode {} - {}'.format(data[0][2:4],  # mode
                                               codes.get(int(data[0][-2:])))  # code
            )
            response = False

        return response


class Proto(Protocols):
    """
        Supports next protocols - PWM, VPW, KWP (from 0 to 5)
    """

    def __init__(self, head=True):
        Protocols.__init__(self)
        self.header = head

    def create_data(self, raw_data):
        data = b''
        if raw_data:
            r_value = self.remove_searching(raw_data)

            if self.check_result(r_value) and self.check_error(r_value):
                if self.header:
                    # multi line response - ELM spec page 42
                    # response format priority:receiver:transmitter:mode:pid:line_number:data:checksum
                    # >0902 - (ex: get VIN)
                    # 86 F1 10 49 02 01 00 00 00 31 FC
                    # 86 F1 10 49 02 02 44 34 47 50 FC
                    # 86 F1 10 49 02 03 30 30 52 35 FC
                    # 86 F1 10 49 02 04 35 42 31 32 FC
                    # 86 F1 10 49 02 05 33 34 35 36 FC
                    if len(r_value) > 1:
                        for item in r_value:
                            # 6: means that we are removed "mode:pid:line" info from the record
                            data += item[12:-2]

                    # single line response
                    elif len(r_value) == 1:
                        r_value = r_value.pop()
                        # removes header and checksum
                        # format priority:receiver:transmitter:mode:pid:data:checksum
                        # [ header][serv][   data   ][CS]
                        # 86 F1 10 41 00 FF FF FF FF FC  - ELM spec page 38
                        data = self.get_data(r_value[6:-2])
                    else:
                        # logging error
                        raise Exception("Error response data")
                else:
                    # multi line response - ELM spec page 42
                    # response format mode:pid:line_number:data
                    # >0902 - (ex: get VIN)
                    # 49 02 01 00 00 00 31
                    # 49 02 02 44 34 47 50
                    # 49 02 03 30 30 52 35
                    # 49 02 04 35 42 31 32
                    # 49 02 05 33 34 35 36
                    if len(r_value) > 1:
                        for item in r_value:
                            # 6: means that we are removed "mode:pid:line" info from the record
                            data += item[6:]

                    # single line response
                    elif len(r_value) == 1:
                        data = self.get_data(r_value.pop())
                    else:
                        # logging error
                        raise Exception("Error response data")

        return data

    @staticmethod
    def get_data(record):
        if len(record) >= 6 and len(record) <= 12:
            # remove first 4 characters. This are service bytes from ELM
            # format mode:pid:data
            # ex: 4100FFFFFFFF - ELM spec page 38
            record = record[4:]
        else:
            # logging error
            raise Exception("The frame size is not suitable.")

        return record


class ProtoCan(Protocols):
    """
        Supports the CAN protocol (from 6 ...)
    """

    def __init__(self, number, head=True):
        """
            :param number - the number of protocol
            :param head - flag for init header
        """
        Protocols.__init__(self)
        self.header = head
        self.mess_SF = 0  # the Single Frame
        self.mess_FF = 1  # the First Frame (of a multiframe message)
        self.mess_CF = 2  # the Consecutive Frame
        # The header bits depends on protocol number.
        # It uses for CAN protocol only
        self.header_bits = self.__get_bits(number)

    def create_data(self, raw_data):
        data = b''
        if raw_data:
            r_value = self.remove_searching(raw_data)

            if self.check_result(r_value) and self.check_error(r_value):
                # if the header enabled
                if self.header:
                    # multi line response - ELM spec page 42
                    # TODO: needs to implement
                    if len(r_value) > 1:
                        pass
                    # single line response
                    elif len(r_value) == 1:
                        if self.header_bits == 11:
                            # format:
                            # 7E8 06 41 00 FF FF FF FF FC
                            type = int(r_value[0][3], 16)

                            # Single Frame
                            if type == self.mess_SF:
                                count_byte = int(r_value[0][4], 16)
                                data = r_value[0][5:5 + count_byte * 2][4:]

                            # the First Frame (of a multiframe message)
                            elif type == self.mess_FF:
                                pass

                            # the Consecutive Frame
                            elif type == self.mess_CF:
                                pass
                    else:
                        # logging error
                        raise Exception("Error response data")
                else:
                    # multi line response - ELM spec page 42
                    # TODO: needs to implement
                    if len(r_value) > 1:
                        pass

                    # single line response
                    elif len(r_value) == 1:
                        pass
                    else:
                        # logging error
                        raise Exception("Error response data")
        return data

    def __get_bits(self, n):
        """
            Retrieves header bits count
            :param n - protocol number
        """
        return self.protocols.get(n)[1] if n else None
