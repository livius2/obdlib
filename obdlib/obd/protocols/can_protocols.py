from obd.protocols.base import Base


class ProtocolsCan(Base):
    """
        Supports the CAN protocol (from 6 ...)
    """

    def __init__(self, number, head=True):
        """
            :param number - the number of protocol
            :param head - flag for init header
        """
        Base.__init__(self)
        self.header = head
        self.add_bits = '00000'
        # message types, see ELM spec. page 44
        self.mess_SF = 0  # the Single Frame
        self.mess_FF = 1  # the First Frame (of a multi frame message)
        self.mess_CF = 2  # the Consecutive Frame
        # The header bits depends on protocol number.
        # It uses for CAN protocol only
        self.header_bits = self.__get_bits(number)
        self.header_11 = 11
        self.header_29 = 29

    def create_data(self, raw_data):
        """
            Analyzes raw data
            :param raw_data - OBDII response
            :return dict
        """
        data = {}
        if raw_data:
            ecu_messages = self.remove_searching(raw_data)

            if self.check_result(ecu_messages) and self.check_error(ecu_messages):
                # if the header enabled
                if self.header:
                    # multi line (ELM spec page 42) or single frame response
                    if len(ecu_messages):
                        # sorts ECU's messages
                        ecu_messages = sorted(ecu_messages)

                        if self.header_bits == self.header_11:
                            # align CAN header (11 bits, 29 bits)
                            # PCI byte are 8 and 9 indexes
                            ecu_messages = [self.add_bits + mess for mess in ecu_messages]

                        for message in ecu_messages:
                            ecu_number = message[6:8]
                            f_type = int(message[8], 16)
                            response_mode = int(message[10:12])

                            # check if response trouble codes
                            if response_mode == 43:
                                # add fake byte after the mode one
                                # nothing to do
                                pass

                            # Single Frame
                            if f_type == self.mess_SF:
                                # 11 bits header:
                                # 7E8 06 41 00 FF FF FF FF FC
                                #
                                # 29 bits header:
                                # 18 DA F1 10 06 41 00 FF FF FF FF FC
                                count_byte = int(message[9], 16)
                                data[ecu_number] = message[10:10 + count_byte * 2][4:]

                            # multi line frame
                            # the First Frame (of a multi frame message)
                            #
                            # 11 bits header:
                            # [ecu][type][order][        data       ]
                            # 7E8    1      0   13 49 04 01 35 36 30
                            # 7E8 21 32 38 39 34 39 41 43
                            # 7E8 22 00 00 00 00 00 00 31
                            #
                            # 29 bits header:
                            # ........[ecu][type][order][       data       ]
                            # 18 DA F1 10    1      0   32 38 39 34 39 41 43
                            # 18 DA F1 10 21 32 38 39 34 39 41 43
                            # 18 DA F1 10 22 00 00 00 00 00 00 31
                            elif f_type == self.mess_FF:
                                data[ecu_number] = message[10:]

                            # the Consecutive Frame
                            elif f_type == self.mess_CF:
                                data[ecu_number] += message[10:]
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
