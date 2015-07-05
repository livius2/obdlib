from obdlib.obd.protocols.main import Main


class Protocols(Main):
    """
        Supports next protocols - PWM, VPW, KWP (from 0 to 5)
    """

    def __init__(self, head=True):
        Main.__init__(self)
        self.header = head

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
                if self.header:
                    if len(ecu_messages):
                        # sorts ECU's messages
                        ecu_messages = sorted(ecu_messages)
                        service_data = self._parse_headers(ecu_messages)
                        for message in ecu_messages:
                            ecu_number = message[4:6]
                            # if one ECU returns multi line
                            # multi line includes line number byte
                            if service_data[ecu_number] > 1:
                                # multi line response - ELM spec page 42
                                # response format priority:receiver:transmitter:mode:pid:line_number:data:checksum
                                # >0902 - (ex: get VIN)
                                # 86 F1 10 49 02 01 00 00 00 31 FC
                                # 86 F1 10 49 02 02 44 34 47 50 FC
                                # 86 F1 10 49 02 03 30 30 52 35 FC
                                # 86 F1 10 49 02 04 35 42 31 32 FC
                                # 86 F1 10 49 02 05 33 34 35 36 FC
                                # 6 * 2: means that we are removed "mode:pid:line" info from the record
                                try:
                                    data[ecu_number] += message[12:-2]
                                except KeyError:
                                    data[ecu_number] = message[12:-2]
                            # frame without line number byte
                            # removes header and checksum
                            # format priority:receiver:transmitter:mode:pid:data:checksum
                            # [ header][serv][   data   ][CS]
                            # 86 F1 10 41 00 FF FF FF FF FC  - ELM spec page 38
                            else:
                                data[ecu_number] = self.get_data(message[6:-2])
                    else:
                        # logging error
                        raise Exception("Error response data")

        return data

    @staticmethod
    def _parse_headers(frames):
        """
            Collects info, how many times ECU met
            :param frames - OBDII response
            :return dict
        """
        ecu_headers = {}
        for mess in frames:
            try:
                ecu_headers[mess[4:6]] += 1
            except KeyError:
                ecu_headers[mess[4:6]] = 1

        return ecu_headers

    @staticmethod
    def get_data(record):
        if len(record) >= 6 and len(record) <= 14:
            # remove first 4 characters. This are service bytes from ELM
            # format mode:pid:data
            # ex: 4100FFFFFFFF - ELM spec page 38
            record = record[4:]
        else:
            # logging error
            raise Exception("The frame size is not suitable.")

        return record
